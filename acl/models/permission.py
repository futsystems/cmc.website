#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.core.exceptions import ValidationError
from config.models import Service
from config.models import ENV_STAGE
from config.models import Service

import logging, traceback
from collections import OrderedDict
logger = logging.getLogger(__name__)
from api_permission import APIPermission
from choices import PERMISSION_TYPE
class Permission(models.Model):
    """
    Permission
    """

    __original_parent = None

    def __init__(self, *args, **kwargs):
        super(Permission, self).__init__(*args, **kwargs)
        self.__original_parent = self.parent


    title = models.CharField('Title', max_length=50, default='Title')
    name = models.CharField('Name', max_length=50, default='Name')

    path = models.CharField('Path', max_length=100, default='', blank=True)
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    type = models.CharField(max_length=20, choices=PERMISSION_TYPE, default='Menu')
    parent = models.ForeignKey('Permission', verbose_name='Parent', related_name='children',
                               on_delete=models.SET_NULL,default=None, blank=True, null=True)

    category = models.CharField('Categoy', max_length=100, default='', blank=True)

    api_permissions = models.ManyToManyField(APIPermission, verbose_name='API Permissions', blank=True)

    relation = models.CharField('Relation', max_length=100, default='', blank=True)
    description = models.CharField('Description', max_length=100, default='', blank=True)

    class Meta:
        app_label = 'acl'

    @property
    def api_permissionns_code(self):
        return [item.code for item in self.api_permissions.all()]

    @property
    def permissionKey(self):
        return self.pk

    def get_relation(self):
       if self.parent is None:
           return self.name
       else:
           return '%s-%s' % (self.parent.get_relation(), self.name)

    def __unicode__(self):
        return u'%s[%s]' % (self.title, self.type)

    def clean(self):
        # 菜单只能在菜单下
        if self.type == 'Menu':
            if self.parent is not None:
                if self.parent.type != 'Menu':
                    raise ValidationError(
                        {'parent': u'父节点:%s不能包含菜单项' % self.parent})

            """
            current = self
            i = 0
            while (current.parent is not None):
                i = i+1
                current = current.parent

            if i > 2:
                raise ValidationError(
                    {'parent': u'菜单层级大于2级'})
            """



        # 页面菜单只能在菜单父节点
        if self.type == 'Page':
            if self.parent is None:
                raise ValidationError(
                    {'parent': u'页面不能作为顶级节点'})
            else:
                if self.parent.type != 'Menu':
                    raise ValidationError(
                        {'parent': u'页面只能在菜单节点下'})

        # 功能节点只能在页面节点下
        if self.type == 'Operation':
            if self.parent is None:
                raise ValidationError(
                    {'parent': u'功能不能作为顶级节点'})
            else:
                if self.parent.type != 'Page':
                    raise ValidationError(
                        {'parent': u'功能节点只能在页面节点下'})


    def save(self, *args, **kwargs):
        self.relation = self.get_relation()
        super(Permission, self).save(*args, **kwargs)

        if self.parent != self.__original_parent:
            #logger.info('save children')
            for item in self.children.all():
                item.save()
        self.__original_parent = self.parent

    def get_dict(self):
        item = {
            'title': self.title,
            'permissionKey': self.permissionKey,
            'name': self.name,
            'path': self.path,
            'children': [child.get_dict() for child in self.children.all()],
            'code': [item.code for item in self.api_permissions.all()],
            'parentId': None if self.parent is None else self.parent.pk,
            'category': self.category,
            'type': self.type

        }
        return item



