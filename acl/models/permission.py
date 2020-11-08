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
from page import Page


class Permission(models.Model):
    """
    Permission
    """

    title = models.CharField('Title', max_length=50, default='Title')
    name = models.CharField('Name', max_length=50, default='Name')

    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    page = models.ForeignKey('Page', verbose_name='Page', related_name='children',
                               on_delete=models.SET_NULL, default=None, blank=True, null=True)

    api_permissions = models.ManyToManyField(APIPermission, verbose_name='API Permissions', blank=True)

    key = models.CharField('Key', max_length=100, default='', blank=True)
    description = models.CharField('Description', max_length=100, default='', blank=True)

    sort = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        app_label = 'acl'
        ordering = ['sort']


    def __unicode__(self):
        return u'%s[%s]' % (self.title, self.key)


    @property
    def group(self):
        if self.page is not None and self.page.group is not None:
            return self.page.group

    @property
    def api_permissionns_name(self):
        return '\n'.join([item.name for item in self.api_permissions.all()])

    @property
    def api_permissionns_code(self):
        return [item.code for item in self.api_permissions.all()]

    def get_key(self):
       if self.page is None:
           return self.name
       else:
           return '%s.%s' % (self.page.get_key(), self.name)


    def copy_to_env(self, env):
        try:
            permission = Permission.objects.get(env=env, key=self.key)
        except Permission.DoesNotExist:
            permission = Permission()

        try:
            page = Page.objects.get(env=env, key=self.page.key)
        except Page.DoesNotExist:
            page = None

        if page is None:
            return

        permission.title = self.title
        permission.name = self.name
        permission.env = env
        permission.page = page

        permission.key = self.key
        permission.description = self.description
        permission.save()

        # udpate api permission code
        codes = APIPermission.objects.filter(env=env, name__in=[item.name for item in self.api_permissions.all()])
        #logger.info(codes)
        for item in codes.all():
            permission.api_permissions.add(item)



    def save(self, *args, **kwargs):
        self.key = self.get_key()
        super(Permission, self).save(*args, **kwargs)


    def get_api_code_info(self):
        item = {
            'pk': self.pk,
            'title': self.title,
            'name': self.name,
            'key': self.key,
            'code': ["%s-%s" % (item.code, item.name) for item in self.api_permissions.all()],

        }
        return item

    def get_dict(self):
        item = {
            'pk': self.pk,
            'title': self.title,
            'name': self.name,
            'key': self.key,
            'type': 'Permission',
            'parentId': None if self.page is None else self.page.pk,
            'code': [item.code for item in self.api_permissions.all()],
            'sort': self.sort

        }
        return item