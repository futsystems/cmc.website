# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.contrib.admin.helpers import ActionForm
from django.contrib import admin,messages
from django.db import connection
from django.utils.html import format_html
from django import forms
from django.shortcuts import render_to_response
from django.db.models import Max

import logging,traceback,json
logger = logging.getLogger(__name__)

import models
from eventbus import EventBublisher
from eventbus import CMCGatewayConfigUpdate
import hashlib


class ApiGatewayConfigAdmin(admin.ModelAdmin):
    list_display = ('version', 'gateway', 'md5', 'date_created','config_action')
    list_filter = ('gateway',)
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        return ['config', 'gateway', 'md5', 'version']

    def config_action(self, obj):
        """

        """
        return format_html(
            '<a class="button" href="{}">Download</a>&nbsp;',
            reverse('admin:config-download', args=[obj.pk]),
        )

    config_action.allow_tags = True
    config_action.short_description = "Action"

    def get_urls(self):
        # use get_urls for easy adding of views to the admin
        urls = super(ApiGatewayConfigAdmin, self).get_urls()
        my_urls = [
            url(
                r'^(?P<gw_config_id>.+)/download/$',
                self.admin_site.admin_view(self.download_config),
                name='config-download',
            ),
        ]

        return my_urls + urls


    def download_config(self, request, gw_config_id):
        gw_config = models.ApiGatewayConfig.objects.get(id=gw_config_id)
        response = HttpResponse(json.dumps(json.loads(gw_config.config), indent=4), content_type='application/txt')
        response['Content-Disposition'] = 'attachment; filename=ocelot_%s_%s.config' % (gw_config.gateway.name, gw_config.version)
        return response


class ApiGatewayAdminForm(forms.ModelForm):
    class Meta:
        model = models.ApiGateway
        exclude = []

    def __init__(self,*args,**kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['default_config'].queryset = models.ApiGatewayConfig.objects.filter(gateway=self.instance)
        self.fields['services'].queryset = models.Service.objects.filter(env=self.instance.env)
        self.fields['service_provider'].queryset = models.Consul.objects.filter(env=self.instance.env)
        self.fields['elastic_apm'].queryset = models.ElastAPM.objects.filter(env=self.instance.env)
        self.fields['event_bus'].queryset = models.EventBus.objects.filter(env=self.instance.env)

class ApiGatewayAdmin(admin.ModelAdmin):
    list_display = ('name', 'gw_type', 'env', 'base_url', 'default_config_title', 'config_action')
    filter_horizontal = ('services', 'other_settings')
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
            '<a class="button" href="{}">Download Draft</a>&nbsp;'
            '<a class="button" href="{}">ConfigSnapshot</a>&nbsp;',
            reverse('admin:config-update', args=[obj.pk]),
            reverse('admin:config-download-draft', args=[obj.pk]),
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
                r'^(?P<gw_id>.+)/download/draft/$',
                self.admin_site.admin_view(self.download_draft),
                name='config-download-draft',
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
        if gw.event_bus is None:
            messages.info(request, "gateway have not set event bus")
            previous_url = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(previous_url)
        EventBublisher(gw.event_bus).send_message(ev)
        messages.info(request, "Send Config Update Success")
        previous_url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_url)

    def download_draft(self, request, gw_id):
        gw = models.ApiGateway.objects.get(id=gw_id)
        response = HttpResponse(json.dumps(gw.generate_ocelot_config(), indent=4), content_type='application/txt')
        response['Content-Disposition'] = 'attachment; filename=ocelot_%s.config' % gw.name
        return response

    def snapshot_config(self, request, gw_id):

        gw = models.ApiGateway.objects.get(id=gw_id)
        config = json.dumps(gw.generate_ocelot_config(), indent=4)
        m = hashlib.md5()
        m.update(config)
        md5 = m.hexdigest()

        args = models.ApiGatewayConfig.objects.filter(gateway=gw)
        max_version = args.aggregate(Max('version'))
        max_version_val = max_version['version__max']
        if max_version_val is  None:
            next_version = '1.0'
        else:
            next_version = str((float(max_version['version__max']) * 10 + 1 )/10)

        # check if config is exist
        if models.ApiGatewayConfig.objects.filter(md5=md5).count() > 0:
            same_config = models.ApiGatewayConfig.objects.filter(md5=md5).first()
            messages.info(request, "Config same with version:%s" % same_config.version)
            previous_url = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(previous_url)

        config_snapshot = models.ApiGatewayConfig.objects.create(gateway=gw, config=config, md5=md5, version=next_version)
        messages.info(request, "Config Snapshot:%s-%s Success" % (config_snapshot.gateway.gateway_schema, config_snapshot.version))
        previous_url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_url)

class ConsulAdmin(admin.ModelAdmin):
    list_display = ('name', 'env', 'host')

    fieldsets = (
        (None, {
            "fields": [
                "name", "env",
            ]
        }),
        ("Config", {
            "fields": [
                "host", "port"
            ]
        }),

        ("Other", {

            "fields": [
                "description"
            ]
        })
    )
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['']
        return ['env']


class ServiceAdminForm(forms.ModelForm):
    class Meta:
        model = models.ApiGateway
        exclude = []

    def __init__(self,*args,**kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        if self.instance.id > 0:
            self.fields['used_services'].queryset = models.Service.objects.filter(env=self.instance.env).exclude(id=self.instance.id)
            self.fields['service_provider'].queryset = models.Consul.objects.filter(env=self.instance.env)
            self.fields['mysql_connections'].queryset = models.MySqlConnection.objects.filter(env=self.instance.env)
            self.fields['elastic_apm'].queryset = models.ElastAPM.objects.filter(env=self.instance.env)
            self.fields['event_bus'].queryset = models.EventBus.objects.filter(env=self.instance.env)




def copy_service_staging(modeladmin, request, queryset):
    for service in queryset.all():
        service.copy_to_env('Staging')
copy_service_staging.short_description = "Copy Service To Staging"

def copy_service_production(modeladmin, request, queryset):
    for service in queryset.all():
        service.copy_to_env('Production')
copy_service_production.short_description = "Copy Service To Production"


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'env', 'service_provider', 'event_bus', 'elastic_apm', 'support_rpc', 'rpc_port', 'support_api', 'api_port')
    ordering = ('name',)
    search_fields = ['name']
    filter_horizontal = ('used_services', 'mysql_connections', 'other_settings')
    list_filter = ('env',)
    form = ServiceAdminForm
    actions = [copy_service_staging, copy_service_production]

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return ((None, {
                    "fields": [
                        "name", "env"
                    ]
                }),

                ("Other", {

                    "fields": [
                        "description"
                    ]
                })
            )

        return (
            (None, {
                "fields": [
                    "name", "env"
                ]
            }),
            ("Services", {
                "fields": [
                    "service_provider", "used_services", "support_rpc", "rpc_port", "support_api", "api_port"
                ]
            }),

            ("Database", {
                "fields": [
                    "mysql_connections"
                ]
            }),

            ("Event", {
                "fields": [
                    "event_bus"
                ]
            }),

            ("Log&Report", {
                "fields": [
                    "elastic_apm", "log_level"
                ]
            }),

            ("Other", {

                "fields": [
                    "other_settings", "description", "pipeline_trigger"
                ]
            })
        )

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['service_provider', 'used_services', 'mysql_connections', 'event_bus', 'elastic_apm']
        return ['env']

class RouteActionForm(ActionForm):
    gateway = forms.CharField()#ChoiceField(widget=forms.Select, choices=models.ApiGateway.objects.all().values_list('id', 'name'), required=True)

def copy_to_gateway(modeladmin, request, queryset):
    gateway = models.ApiGateway.objects.filter(id=request.POST['gateway']).first()
    if gateway is None:
        messages.info(request, "gateway do not exist")
    else:
        for obj in queryset:
            obj.copy_to_gateway(gateway)

class RouteAdminForm(forms.ModelForm):
    class Meta:
        model = models.Route
        exclude = []

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        if self.instance.id > 0:
            self.fields['service'].queryset = models.Service.objects.filter(env=self.instance.env)

class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'env', 'upstream_path_template', 'downstream_path_template', 'priority', 'route_target', 'short_load_balancer',  'authentication_scheme', 'http_handler_options_title')
    list_filter = ('api_gateway', 'service', 'authentication_scheme')
    ordering = ('name',)
    search_fields = ['name', 'upstream_path_template']
    filter_horizontal = ('upstream_http_method', 'upstream_header_transform')
    action_form = RouteActionForm
    actions = [copy_to_gateway]
    form = RouteAdminForm
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

class MySqlConnnectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'env', 'host', 'database', 'user', 'charset', 'is_tracer')
    ordering = ('name',)
    search_fields = ['name']
    fieldsets = (
        (None, {
            "fields": [
                "name", "env", "is_tracer"
            ]
        }),
        ("Config", {
            "fields": [
                "host", "port", "user", "password", "database", "charset"
            ]
        }),

        ("Other", {

            "fields": [
                "description"
            ]
        })
    )
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['']
        return ['env']


class EventBusAdmin(admin.ModelAdmin):
    list_display = ('host', 'env', 'user_name', 'retry_count')
    fieldsets = (
        (None, {
            "fields": [
                "default_subscription_client_name", "env",
            ]
        }),
        ("Config", {
            "fields": [
                "host", "user_name", "password", "retry_count"
            ]
        }),

        ("Other", {

            "fields": [
                "description"
            ]
        })
    )
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['']
        return ['env']

class ElasticAPMAdmin(admin.ModelAdmin):
    list_display = ('service_urls', 'env', 'log_level')

    fieldsets = (
        (None, {
            "fields": [
                "default_service_name", "env",
            ]
        }),
        ("Config", {
            "fields": [
                "service_urls", "log_level"
            ]
        }),

        ("Other", {

            "fields": [
                "description"
            ]
        })
    )
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['']
        return ['env']

class LogItemAdmin(admin.ModelAdmin):
    list_display = ('prefix', 'level')

class LogItemGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('items',)

class SettingGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'description')

class SettingItemAdmin(admin.ModelAdmin):
    list_display = ('setting_group', 'setting_key', 'setting_value', 'description')
    list_filter = ('setting_group',)

admin.site.register(models.ApiGateway, ApiGatewayAdmin)
admin.site.register(models.Consul, ConsulAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Route, RouteAdmin)


admin.site.register(models.HttpHandlerOption, HttpHandlerOptionAdmin)
admin.site.register(models.RateLimitOption, RateLimitOptionAdmin)
admin.site.register(models.HttpMethod, HttpMethodAdmin)
admin.site.register(models.HeaderTransform, HeadTransformAdmin)

admin.site.register(models.ApiGatewayConfig, ApiGatewayConfigAdmin)
admin.site.register(models.MySqlConnection, MySqlConnnectionAdmin)
admin.site.register(models.EventBus, EventBusAdmin)
admin.site.register(models.ElastAPM, ElasticAPMAdmin)

admin.site.register(models.LogItem, LogItemAdmin)
admin.site.register(models.LogItemGroup, LogItemGroupAdmin)

admin.site.register(models.SettingGroup, SettingGroupAdmin)
admin.site.register(models.SettingItem, SettingItemAdmin)