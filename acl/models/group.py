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


class Group(models.Model):
    """
    menu group
    """

    title = models.CharField('Title', max_length=50, default='Title')
    name = models.CharField('Name', max_length=50, default='Name')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    description = models.CharField('Description', max_length=100, default='', blank=True)
    sort = models.PositiveIntegerField(default=0, blank=False, null=False)


    class Meta:
        app_label = 'acl'
        ordering = ['sort']

    def __unicode__(self):
        return u'Group[%s]' % self.title


    def get_dict(self):
        from page import Page
        item = {
            'title': self.title,
            'permissionKey': self.pk,
            'name': self.name,
            #'path': self.path,
            'children': [child.get_dict() for child in self.children.all()],
            #'code': [item.code for item in self.api_permissions.all()],
            #'parentId': None if self.group is None else self.group.pk,
            #'category': self.category,
            'key': self.name,
            'type': 'Group',
            'sort': self.sort

        }
        return item