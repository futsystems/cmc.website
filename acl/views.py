#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from django.shortcuts import render_to_response,render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from models import Permission
from common import Response,Success,Error
import hashlib
from deploy.models import Server
from common.request_helper import get_client_ip
import logging, traceback
from collections import OrderedDict
logger = logging.getLogger(__name__)


def json_response(obj):
    if issubclass(obj.__class__, Response):
        return HttpResponse(json.dumps(obj.to_dict()), content_type="application/json")
    return HttpResponse(json.dumps(obj, indent=4), content_type="application/json")


@csrf_exempt
def sync_permission(request):
    if request.method == "GET":
        return HttpResponse("GET not support")
    else:
        try:
            data = json.loads(request.body)
            system = data['System']
            product = system['Product']
            service = system['Service']
            stage = system['Stage']

            permissions = data['Permissions']

            logger.info('%s %s %s permission cnt:%s' % (product, service, stage, len(permissions)))
            #[Permission.objects.sync_permission(permission) for permission in permissions]
            item = permissions[0]
            Permission.objects.sync_permission(product, service, permissions, stage)
            logger.info(item)
            return json_response(Success())
        except Exception, e:
            logger.error(traceback.format_exc())
            return json_response(Error(e.message))
