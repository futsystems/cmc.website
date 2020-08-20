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

import logging,traceback,json
logger = logging.getLogger(__name__)

import models
from eventbus import EventBublisher
from eventbus import CMCGatewayConfigUpdate


class ApiGatewayConfigAdmin(admin.ModelAdmin):
    list_display = ('version', 'gateway', 'date_created')
    list_filter = ('gateway',)
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        return ['config', 'gateway']

class ApiGatewayAdminForm(forms.ModelForm):
    class Meta:
        model = models.ApiGateway
        exclude = []

    def __init__(self,*args,**kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['default_config'].queryset = models.ApiGatewayConfig.objects.filter(gateway=self.instance)

class ApiGatewayAdmin(admin.ModelAdmin):
    list_display = ('name', 'gw_type', 'env', 'base_url', 'default_config_title', 'config_action')
    form = ApiGatewayAdminForm
    #readonly_fields = ('gw_type','env')

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        return ['gw_type', 'env']

    def config_action(self, obj):
        """

        """
        return format_html(
            '<a class="button" href="{}">Update</a>&nbsp;'
            '<a class="button" href="{}">Download</a>&nbsp;'
            '<a class="button" href="{}">ConfigSnapshot</a>&nbsp;',
            reverse('admin:config-update', args=[obj.pk]),
            reverse('admin:config-download', args=[obj.pk]),
            reverse('admin:config-snapshot', args=[obj.pk]),
        )

    config_action.allow_tags = True
    config_action.short_description = "Action"

    def get_urls(self):
        # use get_urls for easy adding of views to the admin
        urls = super(ApiGatewayAdmin, self).get_urls()
        my_urls = [
            url(
                r'^(?P<gw_id>.+)/update/$',
                self.admin_site.admin_view(self.update_config),
                name='config-update',
            ),

            url(
                r'^(?P<gw_id>.+)/action/$',
                self.admin_site.admin_view(self.download_config),
                name='config-download',
            ),
            url(
                r'^(?P<gw_id>.+)/snapshot/$',
                self.admin_site.admin_view(self.snapshot_config),
                name='config-snapshot',
            ),
        ]

        return my_urls + urls

    def update_config(self, request, gw_id):
        gw = models.ApiGateway.objects.get(id= gw_id)
        ev = CMCGatewayConfigUpdate(gw.gw_type, gw.env)
        EventBublisher().send_message(ev)
        messages.info(request, "Send Config Update Success")
        previous_url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_url)

    def download_config(self, request, gw_id):
        messages.info(request, "demo operation:%s" % gw_id)
        gw = models.ApiGateway.objects.get(id=gw_id)

        response = HttpResponse(json.dumps(gw.get_ocelot_config(),indent=4), content_type='application/txt')
        response['Content-Disposition'] = 'attachment; filename=ocelot_%s.config' % gw.name
        return response

    def snapshot_config(self, request, gw_id):
        messages.info(request, "demo operation:%s" % gw_id)
        gw = models.ApiGateway.objects.get(id=gw_id)
        models.ApiGatewayConfig.objects.create(gateway=gw, config=json.dumps(gw.get_ocelot_config()))
        #response = HttpResponse(json.dumps(gw.get_ocelot_config(),indent=4), content_type='application/txt')
        #response['Content-Disposition'] = 'attachment; filename=ocelot_%s.config' % gw.name
        messages.info(request, "Config Snapshot Success")
        previous_url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_url)

class ConsulAdmin(admin.ModelAdmin):
    list_display = ('name', 'host')


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ['name']

class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'upstream_path_template', 'downstream_path_template', 'priority', 'route_target', 'short_load_balancer',  'authentication_scheme', 'http_handler_options_title')
    list_filter = ('service', 'authentication_scheme')
    ordering = ('name',)
    search_fields = ['name', 'upstream_path_template']

    fieldsets = (
        (None, {
            "fields": [
                "name", "priority", "api_gateway", "description",
            ]
        }),
        ("Upstream", {
            "description": "The information about the license.",
            "fields": [
                "upstream_path_template","upstream_http_method","upstream_header_transform"
            ]
        }),

        ("Downstream", {
            "description": "The information about the hist data service.",
            "fields": [
                "downstream_path_template", "downstream_scheme"
            ]
        }),
        ("Consul", {
            "description": "The information about the hist data service.",
            "fields": [
                "service", "load_balancer"
            ]
        }),
        ("Host Port", {
            "description": "The information about the hist data service.",
            "fields": [
                "downstream_host", "downstream_port"
            ]
        }),

        ("Auth", {
            "description": "The information about the hist data service.",
            "fields": [
                "authentication_scheme", "authorization_scopes"
            ]
        }),

        ("Other Info", {
            "description": "Other Information.",
            'classes': ('collapse',),
            "fields": [
                "rate_limite_options","http_handler_options"
            ]
        }),
    )


class HttpHandlerOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'allow_auto_redirect', 'use_cookie_container', 'user_tracing', 'max_connections_per_server')


class RateLimitOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'client_whitelist', 'enable_rate_limiting', 'period', 'period_timespan', 'limit')

class HttpMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'method')

class HeadTransformAdmin(admin.ModelAdmin):
    list_display = ('name', 'header_key', 'header_value')

admin.site.register(models.ApiGateway, ApiGatewayAdmin)
admin.site.register(models.Consul, ConsulAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Route, RouteAdmin)


admin.site.register(models.HttpHandlerOption, HttpHandlerOptionAdmin)
admin.site.register(models.RateLimitOption, RateLimitOptionAdmin)
admin.site.register(models.HttpMethod, HttpMethodAdmin)
admin.site.register(models.HeaderTransform, HeadTransformAdmin)

admin.site.register(models.ApiGatewayConfig, ApiGatewayConfigAdmin)