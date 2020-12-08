#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from django.shortcuts import render_to_response,render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from common import Response,Success,Error, GitlabAPI
from config import models as config_models
from deploy.models import Deploy
from acl import models as acl_models

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


def diff(request):
    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        env = request.GET.get("env")
        logger.info('get diff of env:%s' % (env))
        if env == None:
            env = 'Staging'
        try:
            if env == 'Staging':
                source = 'Staging'
                target = 'Development'
            elif env == 'Production':
                source = 'Production'
                target = 'Staging'

            # 检查服务变化
            service_diff= diff_service(source, target)

            # 检查路由变化
            route_diff= diff_route(source, target)

            result={
                'service_diff':service_diff,
                'route_diff':route_diff
            }

            logger.info(result)
            return json_response(result)
        except Exception, e:
            logging.error(traceback.format_exc())
            return json_response(Error("get gateway ocelot config error"))

def diff_route(source='Staging',target='Development'):
    target_items = config_models.Route.objects.filter(api_gateway__env=target)
    source_items = config_models.Route.objects.filter(api_gateway__env=source)
    target_names = [item.name for item in target_items]
    source_names = [item.name for item in source_items]

    add_items = list(set(target_names).difference(set(source_names)))
    remove_items = list(set(source_names).difference(set(target_names)))
    intersection_items = list(set(source_names).intersection(set(target_names)))

    diff = {
        'add': add_items,
        'remove': remove_items,
        'diff': []
    }

    for item_name in intersection_items:
        new_item = target_items.get(name=item_name)
        old_item = source_items.get(name=item_name)

        route_diff = diff_route_detail(new_item, old_item)

        if len(route_diff) > 1:
            diff['diff'].append(route_diff)

    return diff

def diff_route_detail(new_route,old_route):
    diff ={
        'name':new_route.name
    }
    if new_route.upstream_path_template != old_route.upstream_path_template:
        diff['upstream_path_template'] = '%s->%s' % (old_route.upstream_path_template, new_route.upstream_path_template)

    if new_route.downstream_path_template != old_route.downstream_path_template:
        diff['downstream_path_template'] = '%s->%s' % (old_route.downstream_path_template, new_route.downstream_path_template)

    if new_route.downstream_scheme != old_route.downstream_scheme:
        diff['downstream_scheme'] = '%s->%s' % (old_route.downstream_scheme, new_route.downstream_scheme)

    if diff_route_detail_service_name(new_route) != diff_route_detail_service_name(old_route):
        diff['service'] = '%s->%s' % (diff_route_detail_service_name(old_route), diff_route_detail_service_name(new_route))


    if new_route.authentication_scheme != old_route.authentication_scheme:
        diff['authentication_scheme'] = '%s->%s' % (old_route.authentication_scheme, new_route.authentication_scheme)

    return diff


def diff_route_detail_service_name(route):
    if route.service is None:
        return None
    else:
        return route.service.name


def diff_service(source='Staging',target='Development'):
    target_items = config_models.Service.objects.filter(env= target)
    source_items = config_models.Service.objects.filter(env= source)
    target_names = [item.name for item in target_items]
    source_names = [item.name for item in source_items]

    add_items = list(set(target_names).difference(set(source_names)))
    remove_items = list(set(source_names).difference(set(target_names)))
    intersection_items = list(set(source_names).intersection(set(target_names)))

    diff = {
        'add': add_items,
        'remove': remove_items,
        'diff': []
    }

    for item_name in intersection_items:
        new_item = target_items.get(name=item_name)
        old_item = source_items.get(name=item_name)

        diff_item = {
            'name': item_name,
            'used_services': diff_service_used_service(new_item, old_item)
        }
        if len(diff_item['used_services']['add']) > 0 or len(diff_item['used_services']['remove']) > 0:
            diff['diff'].append(diff_item)

    return diff


def diff_service_used_service(new_service, old_service):
    """
    检查依赖服务的变化
    """
    listA = [item.name for item in new_service.used_services.all()]
    listB = [item.name for item in old_service.used_services.all()]

    remove = list(set(listB).difference(set(listA)))
    add = list(set(listA).difference(set(listB)))
    return {
        'remove': remove,
        'add': add,
    }


def acl_diff(request):
    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        env = request.GET.get("env")

        if env == None:
            env = 'Staging'
        try:
            if env == 'Staging':
                source = 'Staging'
                target = 'Development'
            elif env == 'Production':
                source = 'Production'
                target = 'Staging'
            logger.info('get diff of env source:%s target:%s' % (source, target))
            # 检查api permission变化
            api_permission_diff= diff_api_permission(source, target)
            group_diff = diff_group(source, target)
            page_diff = diff_page(source, target)
            permission_diff = diff_permission(source, target)
            result={
                'api_permission_diff': api_permission_diff,
                'group_diff': group_diff,
                'page_diff': page_diff,
                'permission_diff': permission_diff
            }

            logger.info(result)
            return json_response(result)
        except Exception, e:
            logging.error(traceback.format_exc())
            return json_response(Error("get gateway ocelot config error"))



def diff_api_permission(source='Staging',target='Development'):
    target_items = acl_models.APIPermission.objects.filter(env= target)
    source_items = acl_models.APIPermission.objects.filter(env= source)
    target_names = [item.name for item in target_items]
    source_names = [item.name for item in source_items]

    add_items = list(set(target_names).difference(set(source_names)))
    remove_items = list(set(source_names).difference(set(target_names)))
    intersection_items = list(set(source_names).intersection(set(target_names)))

    diff = {
        'add': add_items,
        'remove': remove_items,
        'diff': []
    }

    for item_name in intersection_items:
        new_item = target_items.get(name=item_name)
        old_item = source_items.get(name=item_name)

        diff_item = {
            'name': item_name,
        }
        if new_item.code != old_item.code:
            diff_item['code']= '%s->%s' % (old_item.code, new_item.code)
        if new_item.title != old_item.title:
            diff_item['title'] = '%s->%s' % (old_item.title, new_item.title)
        if new_item.group_name != old_item.group_name:
            diff_item['group_name'] = '%s->%s' % (old_item.group_name, new_item.group_name)
        if new_item.group_name != old_item.group_name:
            diff_item['group_name'] = '%s->%s' % (old_item.group_name, new_item.group_name)
        if new_item.service.name != old_item.service.name:
            diff_item['service'] = '%s->%s' % (old_item.service.name, new_item.service.name)


        if len(diff_item) > 1:
            diff['diff'].append(diff_item)

    return diff

def diff_group(source='Staging',target='Development'):
    target_items = acl_models.Group.objects.filter(env= target)
    source_items = acl_models.Group.objects.filter(env= source)
    target_names = [item.name for item in target_items]
    source_names = [item.name for item in source_items]

    add_items = list(set(target_names).difference(set(source_names)))
    remove_items = list(set(source_names).difference(set(target_names)))
    intersection_items = list(set(source_names).intersection(set(target_names)))

    diff = {
        'add': add_items,
        'remove': remove_items,
        'diff': []
    }

    for item_name in intersection_items:
        new_item = target_items.get(name=item_name)
        old_item = source_items.get(name=item_name)

        diff_item = {
            'name': item_name,
        }
        if new_item.title != old_item.title:
            diff_item['title'] = '%s->%s' % (old_item.title, new_item.title)
        if new_item.icon != old_item.icon:
            diff_item['icon'] = '%s->%s' % (old_item.icon, new_item.icon)


        if len(diff_item) > 1:
            diff['diff'].append(diff_item)

    return diff

def diff_page(source='Staging',target='Development'):
    target_items = acl_models.Page.objects.filter(env= target)
    source_items = acl_models.Page.objects.filter(env= source)
    target_names = [item.key for item in target_items]
    source_names = [item.key for item in source_items]

    add_items = list(set(target_names).difference(set(source_names)))
    remove_items = list(set(source_names).difference(set(target_names)))
    intersection_items = list(set(source_names).intersection(set(target_names)))

    diff = {
        'add': add_items,
        'remove': remove_items,
        'diff': [],
    }

    for item_name in intersection_items:
        new_item = target_items.get(key=item_name)
        old_item = source_items.get(key=item_name)

        diff_item = {
            'key': item_name,
        }
        if new_item.title != old_item.title:
            diff_item['title'] = '%s->%s' % (old_item.title, new_item.title)
        if new_item.name != old_item.name:
            diff_item['name'] = '%s->%s' % (old_item.name, new_item.name)
        if new_item.path != old_item.path:
            diff_item['path'] = '%s->%s' % (old_item.path, new_item.path)
        if new_item.group.name != old_item.group.name:
            diff_item['group'] = '%s->%s' % (old_item.group.name, new_item.group.name)
        if new_item.category != old_item.category:
            diff_item['category'] = '%s->%s' % (old_item.category, new_item.category)


        if len(diff_item) > 1:
            diff['diff'].append(diff_item)

    return diff

def diff_permission(source='Staging',target='Development'):
    target_items = acl_models.Permission.objects.filter(env= target)
    source_items = acl_models.Permission.objects.filter(env= source)
    target_names = [item.key for item in target_items]
    source_names = [item.key for item in source_items]

    add_items = list(set(target_names).difference(set(source_names)))
    remove_items = list(set(source_names).difference(set(target_names)))
    intersection_items = list(set(source_names).intersection(set(target_names)))

    diff = {
        'add': add_items,
        'remove': remove_items,
        'diff': [],
    }

    for item_name in intersection_items:
        new_item = target_items.get(key=item_name)
        old_item = source_items.get(key=item_name)

        diff_item = {
            'key': item_name,
            'api_permission': diff_permission_api_permission(new_item, old_item)
        }
        if new_item.title != old_item.title:
            diff_item['title'] = '%s->%s' % (old_item.title, new_item.title)
        if new_item.name != old_item.name:
            diff_item['name'] = '%s->%s' % (old_item.name, new_item.name)
        if new_item.page.key != old_item.page.key:
            diff_item['page'] = '%s->%s' % (old_item.page.key, new_item.page.key)

        if len(diff_item) > 2 or (len(diff_item['api_permission']['add']) > 0 or len(diff_item['api_permission']['remove']) > 0):
            diff['diff'].append(diff_item)

    return diff

def diff_permission_api_permission(new_permission, old_permission):
    """
    检查依赖服务的变化
    """
    listA = [item.name for item in new_permission.api_permissions.all()]
    listB = [item.name for item in old_permission.api_permissions.all()]

    remove = list(set(listB).difference(set(listA)))
    add = list(set(listA).difference(set(listB)))
    return {
        'remove': remove,
        'add': add,
    }


def code_diff(request):
    """
    deploy=WeiShop-Staging:查看测试环境下 代码差异量，显示没有提交到测试环境的commit
        develop 比 master 代码的差异
    deploy=latest_tag:查看发布环境下 代码差异量，显示没有提交到生产环境的commit（已经提交到master，但是没有提打tag）
        master 对 latest_tag的 代码差异
    deploy=WeiShop-1:查看某个部署 代码差异量，显示没有升级到部署的commit
        最新tag的 对部署环境 代码差异
        latest_tag 对 production tag
    :param request:
    :return:
    """
    if request.method == "POST":
        return HttpResponse("POST not support")
    else:
        deploy_key = request.GET.get("deploy")
        try:
            deploy = Deploy.objects.get(key=deploy_key)
        except Deploy.DoesNotExist:
            return json_response(Error("deploy do not exist"))
        if deploy.env == 'Development':
            source = 'Development'
            source_repo = 'develop'
            target = 'Staging'
            target_repo = 'master'
            msg = u'开发环境与测试环境代码差异'
        if deploy.env == 'Staging':
            source = 'Staging'
            source_repo = 'master'
            target = 'Staging'
            target_repo = 'latest_tag'
            msg = u'测试环境与生产环境代码(最新tag版本)代码差异'
        elif deploy.env == 'Production':
            source = 'Staging'
            source_repo = 'latest_tag'
            target = 'Production'
            target_repo = 'product_tag'
            msg = u'某个部署环境与生产环境(最新tag版本)代码差异'
        env = deploy.env

        try:
            logger.info('get code diff from:%s to:%s' % (source_repo, target_repo))
            # 检查api permission变化
            api = GitlabAPI()

            target_items = config_models.Service.objects.filter(env=target)
            source_items = config_models.Service.objects.filter(env=source)
            target_names = [item.name for item in target_items]
            source_names = [item.name for item in source_items]

            add_items = list(set(target_names).difference(set(source_names)))
            remove_items = list(set(source_names).difference(set(target_names)))
            intersection_items = list(set(source_names).intersection(set(target_names)))

            diff = {
                'add': add_items,
                'remove': remove_items,
                'diff': [],
                'msg': msg
            }

            #logger.info(intersection_items)
            idx =0
            for item_name in intersection_items:
                if idx > 1:
                    continue
                new_item = target_items.get(name=item_name)
                old_item = source_items.get(name=item_name)

                path = 'platform/srv.%s' % new_item.name.lower()
                api = GitlabAPI()
                #logger.info('22222')
                # 比较某个部署环境与生产环境(最新tag版本)代码差异
                if deploy.env == 'Production':
                    target_repo = deploy.get_version(old_item.name)

                ret = api.compare_repository(path, source_repo, target_repo)
                if len(ret['commits']) > 0:
                    idx = idx + 1
                    diff['diff'].append({
                        'name': new_item.name,
                        'tags': str.join(',' ,ret['tags']),
                        'path': path,
                        'commits': ret['commits'],
                        'commits_json': json.dumps(ret['commits']),
                        'commit_cnt': len(ret['commits']),
                        'source': ret['source'],
                        'target': ret['target'],
                    })

            #return json_response(diff)
            diff['diff'].sort(key=lambda x: x['name'], reverse=False)
            context = diff

            # Render the HTML template index.html with the data in the context variable
            return render(request, 'update/diff_code.html', context=context)
        except Exception, e:
            logger.error(traceback.format_exc())
            return json_response(Error("get code diff error"))