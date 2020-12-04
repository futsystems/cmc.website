#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from django.shortcuts import render_to_response,render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from models import ApiGateway,Service
from common import Response,Success,Error
import hashlib
from deploy.models import Server
from common.request_helper import get_client_ip
import logging, traceback
from collections import OrderedDict
logger = logging.getLogger(__name__)


def json_response(obj):
    if issubclass(obj.__class__, Response):
        return HttpResponse(json.dumps(obj.to_dict(), ensure_ascii=False, encoding='utf-8').encode('utf-8').decode('unicode_escape'), content_type="application/json")
    return HttpResponse(json.dumps(obj, ensure_ascii=False, indent=4, encoding='utf-8').encode('utf-8').decode('unicode_escape'), content_type="application/json")



def config_gateway(request):
    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        gw_type = request.GET.get("type")
        env = request.GET.get("env")
        logger.info('get config of gateway type:%s env:%s' % (gw_type, env))


        try:
            gw = ApiGateway.objects.filter(env=env, gw_type=gw_type).first()
            if gw is None:
                return json_response(Error("gateway config do not exist"))

            return json_response(gw.get_ocelot_config())
        except Exception, e:
            logging.error(traceback.format_exc())
            return json_response(Error("get gateway ocelot config error"))

def config_gateway_hash(request):
    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        gw_type = request.GET.get("type")
        env = request.GET.get("env")
        logger.info('get config of node:%s env:%s' % (gw_type, env))


        try:
            gw = ApiGateway.objects.filter(env=env, gw_type=gw_type).first()
            if gw is None:
                return json_response(Error("gateway config do not exist"))

            config = json.dumps(gw.get_ocelot_config(), indent=4)
            logging.info('config:%s' % config)

            m = hashlib.md5()
            m.update(config)
            md5 = m.hexdigest()

            return HttpResponse(md5)
        except Exception ,e:
            logging.error(traceback.format_exc())
            return json_response(Error("get gateway config list error"))


def config_gatwway_dotnet(request):
    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        gw_type = request.GET.get("type")
        env = request.GET.get("env")
        logger.info('get config of node:%s env:%s' % (gw_type, env))

        client_ip = get_client_ip(request)
        logger.info('request server config from ip:%s' % client_ip)
        if not Server.objects.in_white_list(client_ip):
            return json_response(Error("ip is not allowed"))
        try:
            gw = ApiGateway.objects.filter(env=env, gw_type=gw_type).first()
            if gw is None:
                return json_response(Error("gateway config do not exist"))

            return json_response(gw.get_config())
        except Exception, e:
            logging.error(traceback.format_exc())
            return json_response(Error("get gateway config list error"))

def config_gatwway_dotnet_hash(request):
    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        gw_type = request.GET.get("type")
        env = request.GET.get("env")
        logger.info('get config of node:%s env:%s' % (gw_type, env))

        client_ip = get_client_ip(request)
        logger.info('request server config from ip:%s' % client_ip)
        if not Server.objects.in_white_list(client_ip):
            return json_response(Error("ip is not allowed"))
        try:
            gw = ApiGateway.objects.filter(env=env, gw_type=gw_type).first()
            if gw is None:
                return json_response(Error("gateway config do not exist"))

            config = json.dumps(gw.get_config(), indent=4)
            logging.info('config:%s' % config)

            m = hashlib.md5()
            m.update(config)
            md5 = m.hexdigest()

            return HttpResponse(md5)
        except Exception,e:
            logging.error(traceback.format_exc())
            return json_response(Error("get gateway config list error"))

def service_list(request):
    try:
        services = Service.objects.filter(env='Development').order_by('name')
        return json_response(Success([item.name for item in services]))
    except Exception,e:
        logging.error(traceback.format_exc())
        return json_response(Error("get service list error"))

def service(request):
    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        client_ip = get_client_ip(request)
        logger.info('request server config from ip:%s' % client_ip)
        if not Server.objects.in_white_list(client_ip):
            return json_response(Error("ip is not allowed"))
        try:
            service_name = request.GET.get("name")
            env = request.GET.get("env")
            ip = request.GET.get("ip", None)
            logger.info('get config of service:%s env:%s' % (service_name, env))

            server = Server.objects.get(ip=ip)

            service = Service.objects.filter(env__iexact=env, name=service_name).first()
            if service is None:
                return json_response(Error("gateway config do not exist"))

            config = json.dumps(service.get_config(ip, server.deploy), indent=4)

            return json_response(service.get_config(ip, server.deploy))
        except Exception, e:
            logging.error(traceback.format_exc())
            return json_response(Error("get service config error"))

def service_hash(request):
    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        client_ip = get_client_ip(request)
        logger.info('request server config from ip:%s' % client_ip)
        if not Server.objects.in_white_list(client_ip):
            return json_response(Error("ip is not allowed"))
        try:
            service_name = request.GET.get("name")
            env = request.GET.get("env")
            ip = request.GET.get("ip", None)
            logger.info('get config hash of service:%s env:%s' % (service_name, env))

            server = Server.objects.get(ip=ip)

            service = Service.objects.filter(env__iexact=env, name=service_name).first()
            if service is None:
                return json_response(Error("gateway config do not exist"))

            config = json.dumps(service.get_config(ip, server.deploy), indent=4, encoding='utf-8').encode('utf-8').decode('unicode_escape')
            logging.info('config:%s' % config)

            m = hashlib.md5()
            m.update(config)
            md5 = m.hexdigest()

            return HttpResponse(md5)

        except Exception,e:
            logging.error(traceback.format_exc())
            return json_response(Error("get service list error"))


def used_services(request):
    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        client_ip = get_client_ip(request)
        logger.info('request server config from ip:%s' % client_ip)
        if not Server.objects.in_white_list(client_ip):
            return json_response(Error("ip is not allowed"))
        try:
            env = request.GET.get("env")
            services = Service.objects.filter(env__iexact=env).order_by('name')
            items = OrderedDict()
            for service in services:
                items[service.name] = [s.name for s in service.used_services.order_by('name')]
            data = OrderedDict()
            data['env'] = env
            data['services'] = items
            return json_response(data)
        except Exception, e:
            logging.error(traceback.format_exc())
            return json_response(Error("get service config error"))
