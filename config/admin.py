# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib import admin,messages
from django.db import connection
from django.utils.html import format_html
from django import forms

import logging,traceback
logger = logging.getLogger(__name__)

import models
from eventbus import EventBublisher
from eventbus import CMCGatewayConfigUpdate





class ApiGatewayAdmin(admin.ModelAdmin):
    list_display = ('name', 'gw_type', 'base_url', 'env', 'is_default', 'config_action')

    def config_action(self, obj):
        """

        """
        return format_html(
            '<a class="button" href="{}">Update</a>&nbsp;'
            '<a class="button" href="{}">Demo</a>&nbsp;',
            reverse('admin:config-update', args=[obj.pk]),
            reverse('admin:config-demo', args=[obj.pk]),
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
                self.admin_site.admin_view(self.demo),
                name='config-demo',
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

    def demo(self, request, gw_id):
        messages.info(request, "demo operation:%s" % gw_id)
        previous_url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_url)

class ConsulAdmin(admin.ModelAdmin):
    list_display = ('name', 'host')


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)

class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'upstream_path_template', 'downstream_path_template', 'priority', 'route_target', 'authentication_scheme', 'http_handel_options_title')
    list_filter = ('service', 'authentication_scheme')
    fieldsets = (
        (None, {
            "fields": [
                "name", "api_gateway", "description",
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