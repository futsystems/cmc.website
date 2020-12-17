#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect, JsonResponse
from django.contrib import admin,messages
from django.utils.html import format_html
from django.forms.models import BaseInlineFormSet
from django import forms
from .. import models
from eventbus import EventBublisher
from eventbus import CMCGatewayConfigUpdate, CMCACLRoleUpdate, CMCACLPermissionUpdate
from config.models import ElastAPM, EventBus, Consul
from common import GitlabAPI, json_response,Error, _json_content
from config import models as config_models
from django.shortcuts import render_to_response,render

import logging,traceback,json
logger = logging.getLogger(__name__)


class VersionInLineFormSet(BaseInlineFormSet):
    def get_queryset(self):
        qs = super(VersionInLineFormSet, self).get_queryset()
        return qs.filter(project=self.instance.project)

class VersionInline(admin.StackedInline):  # or admin.StackedInline
    model = models.Version
    formset = VersionInLineFormSet
    exclude = []

    #filter_horizontal = ('api_permissions',)

class DeployAdminForm(forms.ModelForm):
    class Meta:
        model = models.Server
        exclude = []

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        if self.instance.id > 0:
            self.fields['service_provider'].queryset = Consul.objects.filter(env=self.instance.env)
            self.fields['elastic_apm'].queryset = ElastAPM.objects.filter(env=self.instance.env)
            self.fields['event_bus'].queryset = EventBus.objects.filter(env=self.instance.env)


class DeployAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'env', 'location', 'suffix', 'portal_domain_name', 'gateway_domain_name', 'service_provider', 'elastic_apm', 'event_bus', 'key', 'deploy_action', 'code_action')
    form = DeployAdminForm
    inlines = [VersionInline, ]

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return ((None, {
                    'fields': [
                        'name', 'product_type', 'env', 'location', 'suffix',
                    ]
                }),

                ('Other', {

                    'fields': [
                        'description'
                    ]
                })
            )

        return (
            (None, {
                "fields": [
                    'name', 'product_type', 'env', 'location', 'suffix',
                ]
            }),
            ("Facility", {
                'fields': [
                    'service_provider', 'elastic_apm', 'event_bus',
                ]
            }),

            ("Config", {
                'fields': [
                    'website_domain_name', 'portal_domain_name', 'gateway_domain_name', 'log_level',
                ]
            }),

            ("Miniprogram Template", {
                'fields': [
                    'weixin_miniprogram_template',
                ]
            }),

            ("Other", {

                'fields': [
                    'enable_node_info_filter', 'description'
                ]
            }),

        )

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['service_provider', 'used_services', 'mysql_connections', 'event_bus', 'elastic_apm']
        return ['product_type', 'env', 'location', 'suffix']

    def deploy_action(self, obj):
        """

        """
        return format_html(
            '<a class="button" href="{}">Gateway</a>&nbsp;'
            '<a class="button" href="{}">Permission</a>&nbsp;'
            '<a class="button" href="{}">Role</a>&nbsp;',
            reverse('admin:deploy-update-gateway-config', args=[obj.pk]),
            reverse('admin:deploy-upload-permission', args=[obj.pk]),
            reverse('admin:deploy-upload-role', args=[obj.pk]),
        )

    deploy_action.allow_tags = True
    deploy_action.short_description = "Update Action"

    def code_action(self, obj):
        """

        """
        print obj.env == 'Production'
        if obj.env == 'Production':
            return format_html(
                '<a href="{}" target="_blank">Compare</a>&nbsp;'
                '| <a href="{}" target="_blank">Update Framework</a>&nbsp;'
                '| <a href="{}" target="_blank">Version Diff</a>&nbsp;',
                reverse('admin:deploy-code-compare', args=[obj.pk]),
                reverse('admin:deploy_code_update_framework', args=[obj.pk]),
                reverse('admin:deploy_version_diff', args=[obj.pk]),
            )
        elif obj.env == 'Staging':
            return format_html(
                '<a href="{}" target="_blank">Compare</a>&nbsp;'
                '| <a href="{}" target="_blank">Update Framework</a>&nbsp;',
                reverse('admin:deploy-code-compare', args=[obj.pk]),
                reverse('admin:deploy_code_update_framework', args=[obj.pk]),
            )
        else:
            return format_html(
                '<a href="{}" target="_blank">Compare</a>&nbsp;'
                '| <a href="{}" target="_blank">Update Framework</a>&nbsp;',
                reverse('admin:deploy-code-compare', args=[obj.pk]),
                reverse('admin:deploy_code_update_framework', args=[obj.pk]),
            )

    code_action.allow_tags = True
    code_action.short_description = "Code Action"

    def get_urls(self):
        # use get_urls for easy adding of views to the admin
        urls = super(DeployAdmin, self).get_urls()
        my_urls = [
            url(
                r'^(?P<deploy_id>.+)/upload_permission/$',
                self.admin_site.admin_view(self.upload_permission),
                name='deploy-upload-permission',
            ),
            url(
                r'^(?P<deploy_id>.+)/upload_role/$',
                self.admin_site.admin_view(self.upload_role),
                name='deploy-upload-role',
            ),
            url(
                r'^(?P<deploy_id>.+)/update_gateway_config/$',
                self.admin_site.admin_view(self.update_gateway_config),
                name='deploy-update-gateway-config',
            ),

            url(
                r'^(?P<deploy_id>.+)/code_compare/$',
                self.admin_site.admin_view(self.code_compare),
                name='deploy-code-compare',
            ),
            url(
                r'^(?P<deploy_id>.+)/version_diff/$',
                self.admin_site.admin_view(self.code_confirm),
                name='deploy_version_diff',
            ),
            url(
                r'^(?P<path>.+)/code_merge/$',
                self.admin_site.admin_view(self.code_merge),
                name='deploy-code-merge',
            ),
            url(
                r'^(?P<deploy_id>.+)/code_update_framework/$',
                self.admin_site.admin_view(self.code_update_framework),
                name='deploy_code_update_framework',
            ),
            url(
                r'^(?P<path>.+)/code_tag/$',
                self.admin_site.admin_view(self.code_tag),
                name='deploy-code-tag',
            ),
        ]

        return my_urls + urls

    def code_confirm(self, request, deploy_id):
        deploy = models.Deploy.objects.get(id=deploy_id)
        data = []
        for item in deploy.nodes.all():
            info = {
                'name': item.node_name,
                'version_health': item.version,
                'version': deploy.get_version(item.node_type, item.node_name)
            }
            if not info['version_health'].startswith(item.version):
                data.append(info)
        return json_response(data)

    def code_merge(self,request,path):
        print 'code merge path:%s' % path
        api = GitlabAPI()
        result = api.merge_project(path)
        context ={
            'success': result[0],
            'result': result[1]
        }
        return render(request, 'deploy/admin/merge_result.html', context=context)

    def code_tag(self, request, path):
        print 'code tag path:%s' % path
        api = GitlabAPI()
        result = api.tag_project(path)

        context ={
            'success': result[0],
            'result': result[1]
        }
        return render(request, 'deploy/admin/tag_result.html', context=context)

    def code_update_framework(self, request, deploy_id):
        """
        触发路由更新消息
        """
        previous_url = request.META.get('HTTP_REFERER')
        deploy = models.Deploy.objects.get(id=deploy_id)

        services = config_models.Service.objects.filter(env=deploy.env).all()
        import requests
        import validators
        idx =0;
        for service in services:
            if idx >= 1:
                continue
            if not validators.url(service.pipeline_trigger):
                logger.info('invalid pipeline trigger')
            else:
                result = requests.post(service.pipeline_trigger)
                logger.info('pipline trigger result : %s' % result)
            idx = idx+1

        messages.info(request, "fired runner jobs")
        return HttpResponseRedirect(previous_url)

    def code_compare(self, request, deploy_id):
        """
        比较代码变化
        """
        #previous_url = request.META.get('HTTP_REFERER')
        deploy = models.Deploy.objects.get(id=deploy_id)
        if deploy.env == 'Development':
            source = 'Development'
            source_repo = 'develop'
            target = 'Staging'
            target_repo = 'master'
            msg = u'开发环境与测试环境代码差异'
        if deploy.env == 'Staging':
            source = 'Staging'
            source_repo = 'master'
            target = 'Staging'
            target_repo = 'latest_tag'
            msg = u'测试环境与生产环境代码(最新tag版本)代码差异'
        elif deploy.env == 'Production':
            source = 'Staging'
            source_repo = 'latest_tag'
            target = 'Production'
            target_repo = 'product_tag'
            msg = u'某个部署环境与生产环境(最新tag版本)代码差异'
        try:
            logger.info('get code diff from:%s to:%s' % (source_repo, target_repo))
            # 检查api permission变化
            api = GitlabAPI()

            target_items = config_models.Service.objects.filter(env=target)
            source_items = config_models.Service.objects.filter(env=source)
            target_names = [item.name for item in target_items]
            source_names = [item.name for item in source_items]

            add_items = list(set(target_names).difference(set(source_names)))
            remove_items = list(set(source_names).difference(set(target_names)))
            intersection_items = list(set(source_names).intersection(set(target_names)))

            diff = {
                'add': add_items,
                'remove': remove_items,
                'diff': [],
                'msg': msg,
                'op_tag': deploy.env == 'Staging',
                'op_merge': deploy.env == 'Development',
                'version_id': None
            }

            #logger.info(intersection_items)
            idx =0
            api = GitlabAPI()
            for item_name in intersection_items:
                #if idx > 1:
                #    continue
                new_item = target_items.get(name=item_name)
                old_item = source_items.get(name=item_name)

                path = 'platform/srv.%s' % new_item.name.lower()
                from config.models import GitLabProject
                try:
                    project = GitLabProject.objects.get(path=path)
                except GitLabProject.DoesNotExist, e:
                    return
                project_id =project.project_id
                #logger.info('22222')
                # 比较某个部署环境与生产环境(最新tag版本)代码差异
                if deploy.env == 'Production':
                    target_repo = deploy.get_version('Service', old_item.name)

                ret = api.compare_repository(project_id, source_repo, target_repo)
                tmp = self._parse_compare_result(new_item.name, path, ret)
                if tmp is not None:
                    if deploy.env == 'Production':
                        diff['version_id'] = deploy.get_version_id('Service', old_item.name)
                    diff['diff'].append(tmp)

            #添加 gateway
            name = 'APIGateway'
            path = 'platform/gateway'
            if deploy.env == 'Production':
                target_repo = deploy.get_version('Gateway', 'APIGateway',)
            ret = api.compare_repository(path, source_repo, target_repo)
            tmp = self._parse_compare_result(name, path, ret)
            if tmp is not None:
                if deploy.env == 'Production':
                    diff['version_id'] = deploy.get_version_id('Gateway', 'APIGateway')
                diff['diff'].append(tmp)

            #添加 portal
            name = 'Admin'
            path = 'terminal-portal/admin'
            if deploy.env == 'Production':
                target_repo = deploy.get_version('Portal', 'Admin')
            ret = api.compare_repository(path, source_repo, target_repo)
            tmp = self._parse_compare_result(name, path, ret)
            if tmp is not None:
                if deploy.env == 'Production':
                    diff['version_id'] = deploy.get_version_id('Portal', 'Admin')
                diff['diff'].append(tmp)

            name = 'Console'
            path = 'terminal-portal/console'
            if deploy.env == 'Production':
                target_repo = deploy.get_version('Portal', 'Console')
            ret = api.compare_repository(path, source_repo, target_repo)
            tmp = self._parse_compare_result(name, path, ret)
            if tmp is not None:
                if deploy.env == 'Production':
                    diff['version_id'] = deploy.get_version_id('Portal', 'Console')
                diff['diff'].append(tmp)

            name = 'H5'
            path = 'terminal-portal/h5'
            if deploy.env == 'Production':
                target_repo = deploy.get_version('Portal', 'H5')
            ret = api.compare_repository(path, source_repo, target_repo)
            tmp = self._parse_compare_result(name, path, ret)
            if tmp is not None:
                if deploy.env == 'Production':
                    diff['version_id'] = deploy.get_version_id('Portal', 'H5')
                diff['diff'].append(tmp)


            #return json_response(diff)
            diff['diff'].sort(key=lambda x: x['name'], reverse=False)
            context = diff

            # Render the HTML template index.html with the data in the context variable
            return render(request, 'deploy/admin/diff_code.html', context=context)
        except Exception, e:
            logger.error(traceback.format_exc())
            return json_response(Error('code compare error'))

    def _parse_compare_result(self,name, path, ret):
        if ret is not None and len(ret['commits']) > 0:
            return  {
                'name': name,
                'tags': str.join(',', ret['tags']),
                'path': path,
                'commits': ret['commits'],
                'commits_json': json.dumps(ret['commits']),
                'commit_cnt': len(ret['commits']),
                'source': ret['source'],
                'target': ret['target'],
            }
        else:
            return None

    def update_gateway_config(self, request, deploy_id):
        """
        触发路由更新消息
        """
        previous_url = request.META.get('HTTP_REFERER')
        deploy = models.Deploy.objects.get(id=deploy_id)
        ev = CMCGatewayConfigUpdate(deploy.key)
        if deploy.event_bus is None:
            messages.info(request, "Deploy have not set event bus")
            return HttpResponseRedirect(previous_url)
        EventBublisher(deploy.event_bus).send_message(ev)
        messages.info(request, "Send Gateway Config Update Success")
        return HttpResponseRedirect(previous_url)

    def upload_permission(self, request, deploy_id):
        """
        触发权限更新消息
        """
        previous_url = request.META.get('HTTP_REFERER')
        deploy = models.Deploy.objects.get(id=deploy_id)
        ev = CMCACLPermissionUpdate(deploy.key)
        if deploy.event_bus is None:
            messages.info(request, "Deploy have not set event bus")
            return HttpResponseRedirect(previous_url)
        EventBublisher(deploy.event_bus).send_message(ev)
        messages.info(request, "Send Permission Update Success")
        return HttpResponseRedirect(previous_url)

    def upload_role(self, request, deploy_id):
        """
        触发角色更新消息
        """
        previous_url = request.META.get('HTTP_REFERER')
        deploy = models.Deploy.objects.get(id=deploy_id)
        ev = CMCACLRoleUpdate(deploy.key)
        if deploy.event_bus is None:
            messages.info(request, "Deploy have not set event bus")
            return HttpResponseRedirect(previous_url)
        EventBublisher(deploy.event_bus).send_message(ev)
        messages.info(request, "Send Role Update Success")
        return HttpResponseRedirect(previous_url)



