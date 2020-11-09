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


class BankAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'bank_code')
    ordering = ('bank_code',)


class DeliveryCompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'company_code')
    ordering = ('company_name',)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('region_name', 'region_code', 'parent')
    ordering = ('region_code',)


admin.site.register(models.DeliveryCompany, DeliveryCompanyAdmin)
admin.site.register(models.Bank, BankAdmin)
admin.site.register(models.Region,RegionAdmin)