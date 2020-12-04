#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from django.shortcuts import render_to_response,render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.views.decorators.csrf import csrf_exempt
from deploy.models import Server,Deploy,NodeInfo
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


def node_info(request):

    """
    url = "http://consul.marvelsystem.net:8500/v1/agent/services"
    result = requests.get(url=url)
    # extracting data in json format
    data = result.json()
    list = []
    for key in data:
        if str.endswith(str(data[key]['Service']), 'API'):

            wan = data[key]['TaggedAddresses']['wan_ipv4']
            address = 'http://%s:%s' % (wan['Address'],wan['Port'])
            logger.info('address:%s' % address)
            result = requests.get(url='%s/info' % address)
            list.append(
                {
                    'name': data[key]['Service'],
                    'address':address,
                    'result':result.content
                }
            )
    """

    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        deploy_key = request.GET.get("deploy")
        logger.info('get deploy:%s info' % deploy_key)

        try:
            deploy = Deploy.objects.get(key=deploy_key)
            return json_response(Success(deploy.to_info_dict()))
        except Deploy.DoesNotExist:
            return json_response(Error('Deploy do not exist'))

@csrf_exempt
def register_node_info(request):
    import json
    if request.method == 'POST':
        data = json.loads(request.body)
        logger.info(data)
        try:
            deploy_key = data['Deploy']
            node_service = data['Service']
            ip = get_client_ip(request)

            product_type = data['Product']
            env = data['Env']
            version = data['Version']
            framework = data['Framework']
        except Exception:
            logger.warn('bad register data:%s' % data)

        try:
            deploy = Deploy.objects.get(key=deploy_key)
        except Deploy.DoesNotExist:
            deploy = None
            logger.warn('deploy:%s do not exist' % deploy_key)

        if deploy is not None:
            try:
                node_info = NodeInfo.objects.get(deploy=deploy,node_service=node_service, ip=ip)
            except NodeInfo.DoesNotExist:
                node_info = NodeInfo()
                node_info.node_service = node_service
                node_info.deploy = deploy
                node_info.ip = ip

            node_info.product_type = product_type
            node_info.env = env
            node_info.version = version
            node_info.framework = json.dumps(framework)
            node_info.save()

            logger.warn('service:%s of product:%s in deploy:%s up ' % (node_service, product_type, deploy_key))

    return json_response(Success("success"))

@csrf_exempt
def unregister_node_info(request):
    import json
    if request.method == 'POST':
        data = json.loads(request.body)
        logger.info(data)
        try:
            deploy_key = data['Deploy']
            node_service = data['Service']
            ip = get_client_ip(request)

            product_type = data['Product']
            env = data['Env']
            version = data['Version']
            framework = data['Framework']
        except Exception:
            logger.warn('bad unregister data:%s' % data)

        try:
            deploy = Deploy.objects.get(key=deploy_key)
        except Deploy.DoesNotExist:
            deploy = None
            logger.warn('deploy:%s do not exist' % deploy_key)

        if deploy is not None:
            try:
                node_info = NodeInfo.objects.get(deploy=deploy,node_service=node_service, ip=ip)
            except NodeInfo.DoesNotExist:
                node_info = NodeInfo()
                node_info.node_service = node_service
                node_info.deploy = deploy
                node_info.ip = ip

            node_info.product_type = product_type
            node_info.env = env
            node_info.version = version
            node_info.framework = json.dumps(framework)
            node_info.save()

            logger.warn('service:%s of product:%s in deploy:%s down ' % (node_service, product_type, deploy_key))

    return json_response(Success("success"))

@csrf_exempt
def update_node_info(request):
    import json
    if request.method == 'POST':
        data = json.loads(request.body)
        logger.info(data)
    return json_response(Success("success"))