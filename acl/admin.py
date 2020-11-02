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


class FunctionPermissionAdmin(admin.ModelAdmin):
    list_display = ('permissionId', 'title', 'name', 'path', 'api_permissionns_code', 'env')
    list_filter = ('env',)
    filter_horizontal = ('api_permissions',)
    ordering = ('path',)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        else:
            return ['env']

admin.site.register(models.APIPermission, APIPermissionAdmin)
admin.site.register(models.FunctionPermission, FunctionPermissionAdmin)