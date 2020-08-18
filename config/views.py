#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from django.shortcuts import render_to_response,render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from models import ApiGateway

import logging, traceback
logger = logging.getLogger(__name__)


def json_response(obj):
    return HttpResponse(json.dumps(obj), content_type="application/json")


def config_gateway(request):
    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        gw_type = request.GET.get("type")
        env = request.GET.get("env")
        logger.info('get config of node:%s env:%s' % (gw_type, env))

        dict = {
            'code': 1,
            'msg': 'please provide node and env arguments'
        }

        try:
            gw = ApiGateway.objects.filter(env__iexact=env, gw_type=gw_type, is_default=True).first()
            if gw is None:
                return json_response(dict)

            return json_response(gw.get_ocelot_config())
        except ApiGateway.DoesNotExist:
            return json_response(dict)
