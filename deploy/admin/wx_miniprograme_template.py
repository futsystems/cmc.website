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




