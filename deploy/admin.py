# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.


from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.contrib import admin,messages
from django.db import connection
from django.utils.html import format_html
from django import forms
from django.shortcuts import render_to_response
from django.db.models import Max
from config.models import Service, ApiGateway,Portal

import logging,traceback,json
logger = logging.getLogger(__name__)

import models
from eventbus import EventBublisher
from eventbus import CMCGatewayConfigUpdate,CMCACLRoleUpdate, CMCACLPermissionUpdate
import hashlib
from common import salt_helper
from config.models import ElastAPM, EventBus, Consul

class ServerAdminForm(forms.ModelForm):
    class Meta:
        model = models.Server
        exclude = []

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        if self.instance.id > 0:
            self.fields['installed_services'].queryset = Service.objects.filter(env=self.instance.env)
            self.fields['gateway'].queryset = ApiGateway.objects.filter(env=self.instance.env)
            self.fields['portal'].queryset = Portal.objects.filter(env=self.instance.env)

class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'env', 'deploy', 'node_type', 'ip', 'location', 'host_name', 'function_title', 'salt_action')
    filter_horizontal = ('installed_services', 'installed_services')
    list_filter = ('deploy', 'node_type')
    form = ServerAdminForm
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['installed_services', 'gateway', 'portal']
        else:
            return ['env', 'node_type']

    def salt_action(self, obj):
        """

        """
        if obj.env != 'Production':
            return format_html(
                '<a class="button" href="{}">Highstate</a>&nbsp;'
                '<a class="button" href="{}">Reboot</a>&nbsp;'
                '<a class="button" href="{}">RegisterRunner</a>&nbsp;',
                reverse('admin:salt-highstate', args=[obj.pk]),
                reverse('admin:salt-reboot', args=[obj.pk]),
                reverse('admin:gitlab-register-runner', args=[obj.pk]),
            )
        else:
            return format_html(
                '<a class="button" href="{}">Highstate</a>&nbsp;'
                '<a class="button" href="{}">Reboot</a>&nbsp;',
                reverse('admin:salt-highstate', args=[obj.pk]),
                reverse('admin:salt-reboot', args=[obj.pk]),
            )

    salt_action.allow_tags = True
    salt_action.short_description = "Action"

    def get_urls(self):
        # use get_urls for easy adding of views to the admin
        urls = super(ServerAdmin, self).get_urls()
        my_urls = [
            url(
                r'^(?P<server_id>.+)/highstate/$',
                self.admin_site.admin_view(self.salt_highstate),
                name='salt-highstate',
            ),

            url(
                r'^(?P<server_id>.+)/ping/$',
                self.admin_site.admin_view(self.salt_ping),
                name='salt-ping',
            ),
            url(
                r'^(?P<server_id>.+)/reboot/$',
                self.admin_site.admin_view(self.salt_reboot),
                name='salt-reboot',
            ),
            url(
                r'^(?P<server_id>.+)/register-runner/$',
                self.admin_site.admin_view(self.gitlab_register_runner),
                name='gitlab-register-runner',
            ),
        ]

        return my_urls + urls

    def salt_highstate(self, request, server_id):
        server = models.Server.objects.get(id= server_id)
        messages.info(request, "Hightstate Server:%s" % server.name)
        salt_helper.highstate(server)
        previous_url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_url)

    def salt_ping(self, request, server_id):
        server = models.Server.objects.get(id= server_id)
        result = salt_helper.ping(server)
        messages.info(request, "Ping Server:%s Result:%s" % (server.name, result))

        previous_url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_url)

    def gitlab_register_runner(self, request, server_id):
        server = models.Server.objects.get(id= server_id)
        server.register_runner()
        messages.info(request, "Register Runner Success")
        previous_url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_url)

    def salt_reboot(self, request, server_id):
        server = models.Server.objects.get(id= server_id)
        messages.info(request, "Reboot Server:%s" % server.name)
        salt_helper.reboot(server)
        previous_url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_url)


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
    list_display = ('name', 'product_type', 'env', 'location', 'suffix', 'portal_domain_name', 'gateway_domain_name', 'service_provider', 'elastic_apm', 'event_bus', 'key', 'deploy_action')
    form = DeployAdminForm

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
        ]

        return my_urls + urls

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


admin.site.register(models.Server, ServerAdmin)
admin.site.register(models.Deploy, DeployAdmin)