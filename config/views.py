#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse

from models import ApiGateway,Service
from common import Success, Error, json_response, _json_content_md5
from deploy.models import Server
from common.request_helper import get_client_ip
import logging, traceback
from collections import OrderedDict
logger = logging.getLogger(__name__)


def gateway_config_ocelot(request):
    try:
        config = _get_gateway_config_ocelot(request)
        return json_response(config)
    except Exception, e:
        logger.error(traceback.format_exc())
        return json_response(e.message)


def gateway_config_ocelot_hash(request):
    try:
        config = _get_gateway_config_ocelot(request)
        md5 = _json_content_md5(config)
        return HttpResponse(md5)
    except Exception, e:
        logger.error(traceback.format_exc())
        return json_response(e.message)


def _get_gateway_config_ocelot(request):
    if request.method == "POST":
        raise Exception("POST not support")
    else:
        gw_type = request.GET.get("type")
        env = request.GET.get("env")

        client_ip = get_client_ip(request)
        if not Server.objects.in_white_list(client_ip):
            raise Exception("ip is not allowed")

        logger.info('get gateway ocelot config of type:%s env:%s from ip:%s' % (gw_type, env, client_ip))

        try:
            gw = ApiGateway.objects.filter(env=env, gw_type=gw_type).first()
            return gw.get_ocelot_config()
        except ApiGateway.DoesNotExist:
            raise Exception('gateway:%s do not exist' % gw_type)


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
        ip = request.GET.get("ip", None)
        client_ip = get_client_ip(request)
        if not Server.objects.in_white_list(client_ip):
            raise Exception("ip is not allowed")

        logger.info('get gateway dotnet config of server:%s from ip:%s' % (ip, client_ip))

        # get server from ip
        try:
            server = Server.objects.get(ip=ip)
        except Server.DoesNotExist:
            raise Exception('server:%s do not exist' % ip)

        if server.deploy is None:
            raise Exception("server:%s do not bind deploy info" % ip)

        if server.gateway is None:
            raise Exception("server:%s do not bind gateway info" % ip)

        return server.gateway.get_config(server)


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
        if not Server.objects.in_white_list(client_ip):
            raise Exception("ip:%s is not allowed" % client_ip)

        service_name = request.GET.get("name")
        ip = request.GET.get("ip", None)
        logger.info('get config of service:%s in server:%s from ip:%s' % (service_name, ip, client_ip))

        # get server from ip
        try:
            server = Server.objects.get(ip=ip)
        except Server.DoesNotExist:
            raise Exception('server:%s do not exist' % ip)

        if server.deploy is None:
            raise Exception("server:%s do not bind deploy info" % ip)

        service = Service.objects.filter(env__iexact=server.deploy.env, name=service_name).first()
        if service is None:
            raise Exception("service:%s do not exist" % service_name)

        return service.get_config(server)


def used_services(request):
    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        client_ip = get_client_ip(request)
        logger.info('request server used services config from ip:%s' % client_ip)
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
