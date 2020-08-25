#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from django.shortcuts import render_to_response,render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from deploy.models import Server
from common import Response,Success,Error

import logging, traceback
logger = logging.getLogger(__name__)


def json_response(obj):
    if issubclass(obj.__class__, Response):
        return HttpResponse(json.dumps(obj.to_dict()), content_type="application/json")
    return HttpResponse(json.dumps(obj, indent=4), content_type="application/json")



def salt_pillar(request):
    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        try:
            minion_id = request.GET.get("minion_id")
            logger.info('get pillar of minion id:%s' % minion_id)

            server = Server.objects.get(name__iexact=minion_id)
            if server is None:
                return json_response(Error("minion do not exist"))

            return json_response(server.get_pillar())
        except Exception:
            return json_response(Error("get service list error"))
