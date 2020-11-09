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


class RegionUploadForm(forms.Form):
    csv_file = forms.FileField()

class RegionAdmin(admin.ModelAdmin):
    change_list_template = "basic/admin/change_list.html"
    list_display = ('region_name', 'region_code', 'parent')
    ordering = ('region_code',)

    def get_urls(self):
        urls = super(RegionAdmin, self).get_urls()
        additional_urls = [
            url(
                r'^upload-csv/$',
                self.admin_site.admin_view(self.upload_csv),
                name='upload-region',
            ),
        ]
        return additional_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra = extra_context or {}
        extra["csv_upload_form"] = RegionUploadForm()
        return super(RegionAdmin, self).changelist_view(request, extra_context=extra)

    def upload_csv(self, request):
        previous_url = request.META.get('HTTP_REFERER')
        if request.method == "POST":
            form = RegionUploadForm(request.POST, request.FILES)
            if form.is_valid():
                if request.FILES['csv_file'].name.endswith('csv'):

                    try:
                        decoded_file = request.FILES['csv_file'].read().decode('utf-8')
                    except UnicodeDecodeError as e:
                        self.message_user(
                            request,
                            "There was an error decoding the file:{}".format(e),
                            level=messages.ERROR
                        )
                        return HttpResponseRedirect("..")

                    # Here we will call our class method
                    import csv
                    reader = csv.reader(request.FILES['csv_file'])
                    parent = None
                    parent_code = None
                    for row in reader:
                        if row[2] is None:
                            parent = None

                        else:
                            if parent_code != row[2]:
                                parent_code = row[2]
                                try:
                                    parent = models.Region.objects.get(region_code=parent_code)
                                except models.Region.DoesNotExist:
                                    parent = None



                        model = models.Region.objects.create(region_name=row[0], region_code=row[1],parent=parent)


                    #self.reader = list(csv.DictReader(csv_file, delimiter=','))
                    #result = uploader.create_records()


                else:
                    self.message_user(
                    request,
                    "Incorrect file type: {}".format(
                        request.FILES['csv_file'].name.split(".")[1]
                    ),
                    level=messages.ERROR
                    )

            else:
                self.message_user(
                request,
                "There was an error in the form {}".format(form.errors),
                level=messages.ERROR
                )

        return HttpResponseRedirect("..")


admin.site.register(models.DeliveryCompany, DeliveryCompanyAdmin)
admin.site.register(models.Bank, BankAdmin)
admin.site.register(models.Region, RegionAdmin)
