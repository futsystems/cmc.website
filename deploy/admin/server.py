#!/usr/bin/python
# -*- coding: utf-8 -*-


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

from .. import models
from eventbus import EventBublisher
from eventbus import CMCGatewayConfigUpdate,CMCACLRoleUpdate, CMCACLPermissionUpdate
from common import salt_helper
from config.models import ElastAPM, EventBus, Consul


class ServerAdminForm(forms.ModelForm):
    class Meta:
        model = models.Server
        exclude = []

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        if self.instance.id > 0:
            self.fields['installed_services'].queryset = Service.objects.filter(env=self.instance.deploy.env)
            self.fields['gateway'].queryset = ApiGateway.objects.filter(env=self.instance.deploy.env)
            self.fields['portal'].queryset = Portal.objects.filter(env=self.instance.deploy.env)


class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'deploy', 'node_type', 'ip', 'location', 'host_name', 'function_title', 'salt_action')
    filter_horizontal = ('installed_services', 'installed_services')
    list_filter = ('deploy', 'node_type')
    form = ServerAdminForm

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return ((None, {
                    'fields': [
                        'name', 'location', 'ip', 'deploy', 'node_type'
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
                    'name', 'location', 'ip', 'deploy', 'node_type'
                ]
            }),
            ("Facility", {
                'fields': [
                    'installed_services', 'gateway', 'portal',
                ]
            }),

            ("Components", {
                'classes': ('collapse',),
                'fields': [
                    'install_mysql', 'install_mq', 'install_consul', 'install_apm',
                ]
            }),

            ("Gitlab Runner", {
                'classes': ('collapse',),
                'fields': [
                    'gitlab_runner_register_token', 'gitlab_runner_id', 'gitlab_runner_auth_token',
                ]
            }),

            ("Other", {
                'classes': ('collapse',),
                'fields': [
                    'description'
                ]
            }),

        )

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        else:
            return []

    def salt_action(self, obj):
        """

        """
        if obj.deploy is None:
            return None

        if obj.deploy.env != 'Production':
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

