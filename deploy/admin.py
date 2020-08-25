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
from config.models import Service

import logging,traceback,json
logger = logging.getLogger(__name__)

import models
from eventbus import EventBublisher
from eventbus import CMCGatewayConfigUpdate
import hashlib


class ServerAdminForm(forms.ModelForm):
    class Meta:
        model = models.Server
        exclude = []

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        if self.instance.id > 0:
            self.fields['installed_services'].queryset = Service.objects.filter(env=self.instance.env)


class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'ip')
    filter_horizontal = ('installed_services', 'installed_services')
    form = ServerAdminForm
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['installed_services',]
        return ['env']



admin.site.register(models.Server, ServerAdmin)