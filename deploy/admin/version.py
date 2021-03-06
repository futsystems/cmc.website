#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin,messages
from django.db import connection
from django.utils.html import format_html
from django import forms
from django.shortcuts import render_to_response
from django.db.models import Max
from config.models import Service, ApiGateway,Portal, TagInfo

import logging,traceback,json
logger = logging.getLogger(__name__)

from .. import models


class VersionAdminForm(forms.ModelForm):
    class Meta:
        model = models.Server
        exclude = []

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        if self.instance.id > 0:
            if self.instance.project is not None:
                self.fields['tag'].queryset = TagInfo.objects.filter(project=self.instance.project)

class VersionAdmin(admin.ModelAdmin):
    list_display = ('deploy', 'project', 'tag_name')
    list_filter = ('deploy',)
    form = VersionAdminForm

