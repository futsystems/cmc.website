#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from config.models import Service
from config.models import ENV_STAGE
from config.models import Service

import logging, traceback
from collections import OrderedDict
logger = logging.getLogger(__name__)
from permission import APIPermission

class FunctionPermission(models.Model):
    """
    FunctionPermission
    """
    title = models.CharField('Title', max_length=50, default='Title')
    permission = models.CharField('Permission', max_length=50, default='Title')
    description = models.CharField('Description', max_length=100, default='', blank=True)
    path = models.CharField('Path', max_length=100, default='', blank=True)

    parent = models.ForeignKey('FunctionPermission', verbose_name='Parent', related_name='children',
                               on_delete=models.SET_NULL,default=None, blank=True, null=True)

    api_permissions = models.ManyToManyField(APIPermission, verbose_name='API Permissions', blank=True)
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')


    class Meta:
        app_label = 'acl'

    @property
    def api_permissionns_code(self):
        return [item.code for item in self.api_permissions.all()]

    @property
    def permissionId(self):
        return self.pk

    def get_path(self):
        if self.parent is None:
            return self.permission
        else:
            return '%s.%s' % (self.parent.get_path(), self.permission)

    def __unicode__(self):
        return u'%s-%s' % (self.title, self.permission)

    def save(self, *args, **kwargs):
        logger.info('save operation')
        self.path = self.get_path()
        super(FunctionPermission, self).save(*args, **kwargs)

    def get_dict(self):
        item = {
            'title': self.title,
            'permissionId': self.permissionId,
            'permission': self.permission,
            'path': self.path,
            'childen': [child.get_dict() for child in self.children.all()],
            'api_permissions': [item.permission for item in self.api_permissions.all()]

        }
        return item



