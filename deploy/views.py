#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from django.shortcuts import render_to_response,render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from deploy.models import Server
from common import Response,Success,Error
from common.request_helper import get_client_ip

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
        client_ip = get_client_ip(request)
        logger.info('request server config from ip:%s' % client_ip)
        if not Server.objects.in_white_list(client_ip):
            return json_response(Error("ip is not allowed"))
        try:
            minion_id = request.GET.get("minion_id")
            logger.info('get pillar of minion id:%s' % minion_id)

            server = Server.objects.get(name__iexact=minion_id)
            if server is None:
                return json_response(Error("minion do not exist"))

            return json_response(server.get_pillar())
        except Exception,e:
            logging.error(traceback.format_exc())
            return json_response(Error("get service list error"))


def minion_valid(request, **kwargs):
    """
    验证minion有效性
    利用IP地址来验证 如果配置数据库中有该IP地址则通过否则拒绝
    """
    print 'sss'
    minion_id = kwargs.get('minion_id',None)
    logger.info('Valid minion for id:%s' % minion_id)
    minion = Server.objects.filter(name=minion_id).first()
    if minion is None:
        return json_response(Error("minion do not exist"))
    return json_response(Success('success'))
