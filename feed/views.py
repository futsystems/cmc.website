#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from django.shortcuts import render_to_response,render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.views.decorators.csrf import csrf_exempt
from deploy.models import Server,Deploy,NodeInfo
from common import Response,Success,Error, json_response, _json_content
from common.request_helper import get_client_ip
import requests
import datetime

from models import Article

import logging, traceback
logger = logging.getLogger(__name__)


def index(request):
    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        try:
            type = request.GET.get("type")
            if type is None:
                type = 'All'
            count = request.GET.get("count")
            if count is None:
                count = 10
            count = int(count)
            if count == 0:
                count = 10
            logger.info('get feed of %s count:%s' % (type, count))

            if type != 'All':
                articles = Article.objects.filter(type=type).order_by("create_time").all()[:count]
                data = {}
                data[type.lower()] = [item.to_dict() for item in articles]
                return json_response(data)
            else:
                docs = Article.objects.filter(type='Doc').order_by("create_time").all()[:count]
                news = Article.objects.filter(type='News').order_by("create_time").all()[:count]
                data = {
                    'doc':[item.to_dict() for item in docs],
                    'news': [item.to_dict() for item in news]
                }
                return json_response(data)
        except Exception, e:
            logger.error(traceback.format_exc())
            return json_response(Error("get feed error"))