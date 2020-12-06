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


class IPAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'is_blocked')

