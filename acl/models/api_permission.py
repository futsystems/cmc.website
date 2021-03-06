#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from config.models import Service
from config.models import ENV_STAGE
from config.models import Service

import logging, traceback
from collections import OrderedDict
logger = logging.getLogger(__name__)

class APIPermissionManager(models.Manager):
    def sync_permission(self, product_name, service_name, permissions, stage='Development'):

        service = Service.objects.get(name=service_name, env=stage)
        if service is None:
            raise Exception(u"service:%s do not exist" % service_name)

        # 将本次需要更新的权限同步标识更新为False
        APIPermission.objects.filter(service=service, env=stage).update(synced=False)

        logger.info(service)

        for permission in permissions:
            logger.info(permission)
            try:
                item = APIPermission.objects.get(name=permission['Name'], service=service, env=stage)

                item.code = permission['Code']
                item.title = permission['Title']
                item.group_name = permission['GroupName']
                item.description = permission['Description']
                item.synced = True
                item.save()

            except APIPermission.DoesNotExist:
                APIPermission.objects.create(name=permission['Name'],
                                          code=permission['Code'],
                                          title=permission['Title'],
                                          group_name=permission['GroupName'],
                                          description=permission['Description'],
                                          service=service,
                                          env=stage,
                                          )

        # 过滤出没有更新的权限(权限调整去除的权限项)并删除
        APIPermission.objects.filter(service=service, env=stage, synced=False).delete()



class APIPermission(models.Model):
    """
    permission
    """
    title = models.CharField('Title', max_length=50, default='Title')
    group_name = models.CharField('Group Name', max_length=50, default='GroupName')
    description = models.CharField('Description', max_length=100, default='', blank=True)
    name = models.CharField('Name', max_length=50, default='Name')
    code = models.IntegerField('Code', default=0)

    service = models.ForeignKey(Service, related_name='permissions', verbose_name='Service', on_delete=models.CASCADE,
                                default=None, blank=True, null=True)

    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    synced = models.BooleanField('Sync', default=True)

    objects = APIPermissionManager()

    class Meta:
        app_label = 'acl'

    def get_dict(self):
        item = {
            'title': self.title,
            'group_name': self.group_name,
            'description': self.description,
            'name': self.name,
            'code': self.code,
            'service': self.service.name,
        }
        return item

    def copy_to_env(self, env):
        try:
            api_permission = APIPermission.objects.get(env=env, name=self.name)
        except APIPermission.DoesNotExist:
            api_permission = APIPermission()

        try:
            service = Service.objects.get(env=env, name=self.service.name)
        except Service.DoesNotExist:
            service = None

        if service is None:
            return

        api_permission.title = self.title
        api_permission.group_name = self.group_name
        api_permission.description = self.description
        api_permission.name = self.name
        api_permission.code = self.code

        api_permission.service = service

        api_permission.env = env
        api_permission.synced = self.synced
        api_permission.save()


    def __unicode__(self):
        return u'%s-%s' % (self.name, self.code)

