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
from eventbus import CMCGatewayConfigUpdate
import hashlib
from common import  salt_helper


class APIPermissionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'title', 'group_name', 'description', 'service', 'env')
    list_filter = ('env', 'service')
    ordering = ('code',)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        else:
            return ['env', 'service']


class PermissionlInline(SortableInlineAdminMixin, admin.TabularInline):  # or admin.StackedInline
    model = models.Permission

class PageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'name', 'path', 'group', 'permissions', 'category', 'key',  'env')
    list_filter = ('env',)
    ordering = ('sort',)
    #inlines = (PermissionlInline,)
    #change_list_template = 'admin/list.html'

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['key']
        else:
            return ['env', 'key']

class GroupAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'name',  'env')
    list_filter = ('env',)
    ordering = ('sort',)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        else:
            return ['env']

class PermssionAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'name', 'page', 'key', 'api_permissionns_code', 'env')
    list_filter = ('env',)
    filter_horizontal = ('api_permissions',)
    ordering = ('sort',)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        else:
            return ['env']

admin.site.register(models.APIPermission, APIPermissionAdmin)
admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.Page, PageAdmin)
admin.site.register(models.Permission, PermssionAdmin)