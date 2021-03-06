#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from django.shortcuts import render_to_response,render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from models import APIPermission, Page,Permission,Group, Role
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
            APIPermission.objects.sync_permission(product, service, permissions, stage)
            logger.info(item)
            return json_response(Success())
        except Exception, e:
            logger.error(traceback.format_exc())
            return json_response(Error(e.message))



def permission(request):
    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        env = request.GET.get("env")
        logger.info('get permission of env:%s' % (env))

        try:
            groups = Group.objects.filter(env=env,enable=True)
            return json_response([item.get_dict() for item in groups])
        except Exception, e:
            logging.error(traceback.format_exc())
            return json_response(Error("get gateway ocelot config error"))

def role(request):
    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        env = request.GET.get("env")
        logger.info('get role of env:%s' % (env))

        try:
            roles = Role.objects.filter(env=env)
            return json_response([item.get_dict() for item in roles])
        except Exception, e:
            logging.error(traceback.format_exc())
            return json_response(Error("get gateway ocelot config error"))

def permission_used(request):
    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        env = request.GET.get("env")
        service = request.GET.get("service")
        logger.info('get permssions used  of service:%s env:%s' % (service, env))

        api_permissions = APIPermission.objects.filter(service__name=service,env=env)

        #for code in api_permissions:
        permissions = Permission.objects.filter(api_permissions__in=api_permissions).distinct()


        logger.info(permissions)

        return json_response([item.get_api_code_info() for item in permissions])

def api_permission(request):
    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        env = request.GET.get("env")
        logger.info('get permission of env:%s' % env)

        try:
            permissions = APIPermission.objects.filter(env=env)

            return json_response([perm.get_dict() for perm in permissions])
        except Exception, e:
            logging.error(traceback.format_exc())
            return json_response(Error("get gateway ocelot config error"))
