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


def demo(request):
    api = GitlabAPI()
    projects = api.get_projects()
    from config.models import GitLabProject
    logger.info(projects)
    for item in projects:
        project = GitLabProject()
        project.path = item['path']
        project.project_id = item['project_id']
        project.save()

def demo2(request):
    from config.models import GitLabProject,TagInfo
    api = GitlabAPI()
    for project in GitLabProject.objects.all():
        item = api.get_project_by_id(project.project_id)
        for tag in item.tags.list():
            info = TagInfo()
            info.project = project
            info.tag = tag.name
            info.version = tag.name[1:]
            info.db_version = 0
            info.save()

        tags = item.tags.list()
        logger.info('project:%s tags:%s' % (project.path, [tag.name for tag in tags]))



