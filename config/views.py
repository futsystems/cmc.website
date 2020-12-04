#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response,render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from models import ApiGateway,Service
from common import Response,Success,Error,json_response, _json_content, _json_content_md5
import hashlib
from deploy.models import Server
from common.request_helper import get_client_ip
import logging, traceback
from collections import OrderedDict
logger = logging.getLogger(__name__)


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
            logger.error(traceback.format_exc())
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

            config = _json_content(gw.get_ocelot_config())
            logging.info('config:%s' % config)

            m = hashlib.md5()
            m.update(config)
            md5 = m.hexdigest()

            return HttpResponse(md5)
        except Exception ,e:
            logger.error(traceback.format_exc())
            return json_response(Error("get gateway config list error"))


def gatwway_config_dotnet(request):
        try:
            config = _get_gateway_config_dotnet(request)
            return json_response(config)
        except Exception, e:
            logger.error(traceback.format_exc())
            return json_response(e.message)

def gatwway_config_dotnet_hash(request):
    try:
        config = _get_gateway_config_dotnet(request)
        md5 = _json_content_md5(config)
        return HttpResponse(md5)
    except Exception, e:
        logger.error(traceback.format_exc())
        return json_response(e.message)


def _get_gateway_config_dotnet(request):
    if request.method == "POST":
        raise Exception("POST not support")
    else:
        gw_type = request.GET.get("type")
        env = request.GET.get("env")
        logger.info('get gateway config of type:%s env:%s' % (gw_type, env))

        client_ip = get_client_ip(request)
        logger.info('request server config from ip:%s' % client_ip)
        if not Server.objects.in_white_list(client_ip):
            raise Exception("ip is not allowed")

        try:
            gw = ApiGateway.objects.filter(env=env, gw_type=gw_type).first()
            return gw.get_config()
        except ApiGateway.DoesNotExist:
            raise Exception('gateway:%s do not exist' % gw_type)



def service_list(request):
    try:
        services = Service.objects.filter(env='Development').order_by('name')
        return json_response(Success([item.name for item in services]))
    except Exception,e:
        logging.error(traceback.format_exc())
        return json_response(Error("get service list error"))


def service(request):
    try:
        config = _get_service_config(request)
        return json_response(config)
    except Exception, e:
        logger.error(traceback.format_exc())
        return json_response(Error(e.message))


def service_hash(request):
    try:
        config = _get_service_config(request)
        md5 = _json_content_md5(config)
        return HttpResponse(md5)
    except Exception, e:
        logger.error(traceback.format_exc())
        return json_response(Error(e.message))


def _get_service_config(request):
    """
    get service config
    :param request:
    :return:
    """
    if request.method == "POST":
        raise Exception("POST not support")
    else:
        client_ip = get_client_ip(request)
        logger.info('request server config from ip:%s' % client_ip)
        if not Server.objects.in_white_list(client_ip):
            raise Exception("ip is not allowed")

        service_name = request.GET.get("name")
        env = request.GET.get("env")
        ip = request.GET.get("ip", None)
        logger.info('get config of service:%s env:%s' % (service_name, env))

        server = Server.objects.get(ip=ip)
        if server is None:
            raise Exception("server:%s do not exist" % ip)

        service = Service.objects.filter(env__iexact=env, name=service_name).first()
        if service is None:
            raise Exception("service:%s do not exist" % service_name)

        return service.get_config(ip, server.deploy)





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
            logger.error(traceback.format_exc())
            return json_response(Error("get service config error"))
