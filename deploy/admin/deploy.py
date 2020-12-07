#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect, JsonResponse
from django.contrib import admin,messages
from django.utils.html import format_html
from django import forms
from .. import models
from eventbus import EventBublisher
from eventbus import CMCGatewayConfigUpdate, CMCACLRoleUpdate, CMCACLPermissionUpdate
from config.models import ElastAPM, EventBus, Consul

import logging,traceback,json
logger = logging.getLogger(__name__)


class VersionInline(admin.StackedInline):  # or admin.StackedInline
    model = models.Version
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

            ("Portal Tag", {
                'fields': [
                    'portal_admin_tag', 'portal_console_tag', 'portal_h5_tag',
                ]
            }),

            ("Other", {

                'fields': [
                    'description'
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
        return format_html(
            '<a href="{}" target="_blank">Compare</a>&nbsp;',
            reverse('admin:deploy-code-compare', args=[obj.pk]),
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
        ]

        return my_urls + urls

    def code_compare(self, request, deploy_id):
        """
        比较代码变化
        """
        previous_url = request.META.get('HTTP_REFERER')
        deploy = models.Deploy.objects.get(id=deploy_id)
        if deploy.env == 'Development':
            messages.info(request, "Development has no target to compare")
            return HttpResponseRedirect(previous_url)

        if deploy.env == 'Staging':
            url = '/update/diff/code/?deploy=%s' % deploy.key
            return HttpResponseRedirect(url)

        if deploy.env == 'Production':
            url = '/update/diff/code/?deploy=%s' % deploy.key
            return HttpResponseRedirect(url)

        messages.info(request, "No target to compare")
        return HttpResponseRedirect(previous_url)



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



