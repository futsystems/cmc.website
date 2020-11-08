#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.


from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.contrib import admin,messages
from adminsortable2.admin import SortableAdminMixin,SortableInlineAdminMixin

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
from eventbus import CMCGatewayConfigUpdate, CMCACLPermissionUpdate
import hashlib
from common import  salt_helper


class ServiceListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Service'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'service_name'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list = [(item.name, item.name) for item in Service.objects.all()]
        # 去重
        func = lambda x, y: x if y in x else x + [y]
        return  reduce(func, [[], ] + list)


    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        #logger.info('value:%s' % self.value())
        # to decide how to filter the queryset.
        if self.value() is not None:
            return queryset.filter(service__name=self.value())

def copy_api_permission_staging(modeladmin, request, queryset):
    for item in queryset.all():
        item.copy_to_env('Staging')
copy_api_permission_staging.short_description = "Copy API Permission To Staging"

class APIPermissionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'title', 'group_name', 'description', 'service', 'env')
    list_filter = ('env', ServiceListFilter)
    ordering = ('code',)
    actions = [copy_api_permission_staging]

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        else:
            return ['env', 'service']


class PermissionlInline(SortableInlineAdminMixin, admin.StackedInline):  # or admin.StackedInline
    model = models.Permission
    filter_horizontal = ('api_permissions',)

class GropListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Group'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'group_name'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list = [(item.name, item.title) for item in models.Group.objects.all()]
        # 去重
        func = lambda x, y: x if y in x else x + [y]
        return  reduce(func, [[], ] + list)


    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        #logger.info('value:%s' % self.value())
        # to decide how to filter the queryset.
        if self.value() is not None:
            return queryset.filter(group__name=self.value())


def copy_page_staging(modeladmin, request, queryset):
    for page in queryset.all():
        page.copy_to_env('Staging')
copy_page_staging.short_description = "Copy Page To Staging"

class PageAdminForm(forms.ModelForm):
    class Meta:
        model = models.Page
        exclude = []

    def __init__(self,*args,**kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        if self.instance.id > 0:
            self.fields['group'].queryset = models.Group.objects.filter(env=self.instance.env)

class PageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'name', 'path', 'group', 'permissions', 'category', 'key', 'enable', 'env')
    list_filter = ('env', GropListFilter)
    ordering = ('sort',)
    inlines = (PermissionlInline,)
    actions = [copy_page_staging]
    form = PageAdminForm
    #change_list_template = 'admin/list.html'


    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['key']
        else:
            return ['env', 'key']

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return (("Basic", {
                    "fields": [
                        "title", "name", "env"
                    ]
                }),
            )

        return (("Basic", {
                    "fields": [
                        "title", "name", "env", "path", "group", "category"
                    ]
                }),

                ("Other", {

                    "fields": [
                        "key", "description"
                    ]
                })
            )

def copy_group_staging(modeladmin, request, queryset):
    for group in queryset.all():
        group.copy_to_env('Staging')
copy_group_staging.short_description = "Copy Group To Staging"

class GroupAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'name', 'enable', 'env')
    list_filter = ('env',)
    ordering = ('sort',)
    change_list_template = 'acl/admin/change_list.html'
    actions = [copy_group_staging]

    def get_urls(self):
        urls = super(GroupAdmin, self).get_urls()
        my_urls = [
            url(
                r'^sync_permission/$',
                self.admin_site.admin_view(self.sync_view),
                name='sync_permission',
            ),
        ]
        return my_urls + urls

    def sync_view(self, request):
        # custom view which should return an HttpResponse
        previous_url = request.META.get('HTTP_REFERER')
        #ev = CMCACLPermissionUpdate('Development')
        #if gw.event_bus is None:
        #    messages.info(request, "gateway have not set event bus")
        #    previous_url = request.META.get('HTTP_REFERER')
        #    return HttpResponseRedirect(previous_url)
        #EventBublisher(gw.event_bus).send_message(ev)
        #messages.info(request, "Send Config Update Success")
        #previous_url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_url)
        pass
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        else:
            return ['env']

class PermissionAdminForm(forms.ModelForm):
    class Meta:
        model = models.Page
        exclude = []

    def __init__(self,*args,**kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        if self.instance.id > 0:
            self.fields['page'].queryset = models.Page.objects.filter(env=self.instance.env)

class PermissionGroupListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Group'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'group_name'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list = [(item.name, item.title) for item in models.Group.objects.all()]
        # 去重
        func = lambda x, y: x if y in x else x + [y]
        return  reduce(func, [[], ] + list)


    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        #logger.info('value:%s' % self.value())
        # to decide how to filter the queryset.
        if self.value() is not None:
            return queryset.filter(page__group__name=self.value())


def copy_permission_staging(modeladmin, request, queryset):
    for page in queryset.all():
        page.copy_to_env('Staging')
copy_permission_staging.short_description = "Copy Permission To Staging"


class PermssionAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'name', 'page', 'group', 'key', 'permission_code_title','description', 'env')
    list_filter = ('env', PermissionGroupListFilter)
    filter_horizontal = ('api_permissions',)
    ordering = ('sort',)
    search_fields = ('key',)
    form = PermissionAdminForm
    actions = [copy_page_staging]

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        else:
            return ['env']

    def permission_code_title(self, instance):
        return format_html(
            '<div title="{}" style="width:200px;word-break:break-word">{}</div>',
            instance.api_permissionns_name,
            ','.join([str(item) for item in instance.api_permissionns_code])
        )

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return (("Basic", {
                    "fields": [
                        "title", "name", "env"
                    ]
                }),
            )

        return (("Basic", {
                    "fields": [
                        "title", "name", "env", "page", "api_permissions"
                    ]
                }),

                ("Other", {

                    "fields": [
                        "key", "description"
                    ]
                })
            )


class RoleAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'key', 'description', 'env')
    list_filter = ('env',)
    filter_horizontal = ('permissions',)
    #inlines = (PermissionlInline,)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        else:
            return ['env']

admin.site.register(models.APIPermission, APIPermissionAdmin)
admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.Page, PageAdmin)
admin.site.register(models.Permission, PermssionAdmin)
admin.site.register(models.Role, RoleAdmin)