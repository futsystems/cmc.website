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
import requests


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
        if not Server.objects.in_white_list(client_ip):
            return json_response(Error("ip is not allowed"))
        try:
            minion_id = request.GET.get("minion_id")
            logger.info('get pillar of minion id:%s from ip:%s' % (minion_id, client_ip))

            try:
                server = Server.objects.get(name__iexact=minion_id)
            except Server.DoesNotExist:
                return json_response(Error("minion:%s do not exist" % minion_id))
            return json_response(server.get_pillar())
        except Exception, e:
            logger.error(traceback.format_exc())
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


def node_info2(request):
    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        deploy_key = request.GET.get("deploy")
        logger.info('get deploy:%s info' % deploy_key)

        try:
            deploy = Deploy.objects.get(key=deploy_key)
            #url = "http://%s:8500/v1/agent/services" % deploy.service_provider.host
            url2 = 'http://%s:8500/v1/health/node/consul-%s' % (deploy.service_provider.host, deploy.key)
            logger.info('url:%s' % url2)
            result = requests.get(url=url2)

            return json_response(Success(result.json()))
        except Deploy.DoesNotExist:
            return json_response(Error('Deploy do not exist'))

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
            data = deploy.to_info_dict()

            try:
                url2 = 'http://%s:8500/v1/health/node/consul-%s' % (deploy.service_provider.host, deploy.key)
                logger.info('url:%s' % url2)
                health_result = requests.get(url=url2).json()

                for node in data['nodes']:
                    node['healths'] = get_health_result(health_result, node['service'])
            except Exception:
                logging.error(traceback.format_exc())
            return json_response(Success(data))
        except Deploy.DoesNotExist:
            return json_response(Error('Deploy do not exist'))

def get_health_result(health_result,service_name):
    api_name = '%sAPI' % service_name
    rpc_name = '%sRPC' % service_name
    result = []
    for item in health_result:
        #logger.info(item)
        #logger.info(item['ServiceName'])
        if item['ServiceName'] == api_name:
            result.append({
                'service_name':api_name,
                'status': item['Status'],
                'output': item['Output'],
                'type': item['Type'],
                'notes': item['Notes'],
            })
        if item['ServiceName'] == rpc_name:
            result.append({
                'service_name': item['ServiceName'],
                'status': item['Status'],
                'output': item['Output'],
                'type': item['Type'],
                'notes': item['Notes'],
            })
    return result

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
            node_info.up = True
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
            node_info.up = False
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