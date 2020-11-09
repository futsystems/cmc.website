#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from django.shortcuts import render_to_response,render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from models import Bank
from common import Response,Success,Error
import hashlib
from deploy.models import Server
from common.request_helper import get_client_ip
import logging, traceback
from collections import OrderedDict
logger = logging.getLogger(__name__)


def json_response(obj):
    if issubclass(obj.__class__, Response):
        return HttpResponse(json.dumps(obj.to_dict(), ensure_ascii=False), content_type="application/json")
    return HttpResponse(json.dumps(obj, indent=4, ensure_ascii=False), content_type="application/json")


def bank(request):
    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        logger.info('get bank list')

        try:
            banks = Bank.objects.all()
            return json_response([item.get_dict() for item in banks])
        except Exception, e:
            logging.error(traceback.format_exc())
            return json_response(Error("get bank ocelot config error"))