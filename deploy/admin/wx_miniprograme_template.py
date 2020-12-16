#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin,messages
from django.core.urlresolvers import reverse
from django.conf.urls import url
from django.db import connection
from django.utils.html import format_html
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect, JsonResponse

from django import forms
from django.shortcuts import render_to_response
from django.db.models import Max
from config.models import Service, ApiGateway,Portal, TagInfo

import logging,traceback,json
logger = logging.getLogger(__name__)

from .. import models


class WeiXinMiniprogramTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'app_id', 'web_hook', 'latest_version', 'template_action')

    def template_action(self, obj):
        """

        """
        return format_html(
            '<a class="button" href="{}">Release</a>&nbsp;',
            reverse('admin:deploy_wx_template_release_new', args=[obj.pk]),
        )

    template_action.allow_tags = True
    template_action.short_description = "Template Action"


    def get_urls(self):
        # use get_urls for easy adding of views to the admin
        urls = super(WeiXinMiniprogramTemplateAdmin, self).get_urls()
        my_urls = [
            url(
                r'^(?P<template_config_id>.+)/new_release/$',
                self.admin_site.admin_view(self.release_new),
                name='deploy_wx_template_release_new',
            ),
        ]

        return my_urls + urls

    def release_new(self, request, template_config_id):
        """
        触发路由更新消息
        """
        previous_url = request.META.get('HTTP_REFERER')
        wx_template = models.WeiXinMiniprogramTemplate.objects.get(id=template_config_id)
        result = wx_template.release()
        if result['code'] > 0:
            messages.info(request, result['msg'])
        else:
            messages.info(request, 'release miniprogram template:%s success' % result['data'])
        return HttpResponseRedirect(previous_url)

