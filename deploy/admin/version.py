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


class VersionAdminForm(forms.ModelForm):
    class Meta:
        model = models.Server
        exclude = []

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        if self.instance.id > 0:
            self.fields['node_name'].queryset = Service.objects.filter(env=self.instance.deploy.env)

class VersionAdmin(admin.ModelAdmin):
    list_display = ('deploy', 'node_type', 'node_name', 'version')
    list_filter = ('deploy',)
    form = VersionAdminForm

