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
from group import Group

class Page(models.Model):
    """
    Permission
    """


    title = models.CharField('Title', max_length=50, default='Title')
    name = models.CharField('Name', max_length=50, default='Name')

    path = models.CharField('Path', max_length=100, default='', blank=True)
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')

    group = models.ForeignKey('Group', verbose_name='Group', related_name='children',
                               on_delete=models.SET_NULL, default=None, blank=True, null=True)

    category = models.CharField('Categoy', max_length=100, default='', blank=True)

    #api_permissions = models.ManyToManyField(APIPermission, verbose_name='API Permissions', blank=True)

    key = models.CharField('Key', max_length=100, default='', blank=True)
    description = models.CharField('Description', max_length=100, default='', blank=True)

    sort = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        app_label = 'acl'
        ordering = ['sort']

    @property
    def permissions(self):
        return [item.name for item in self.children.all()]

    def get_key(self):
       if self.group is None:
           return self.name
       else:
           return '%s.%s' % (self.group.name, self.name)

    def __unicode__(self):
        return u'%s[%s]' % (self.title, self.name)

    def save(self, *args, **kwargs):
        self.key = self.get_key()
        super(Page, self).save(*args, **kwargs)

    def get_dict(self):
        item = {
            'id': self.pk,
            'title': self.title,
            'name': self.name,
            'path': self.path,
            'key': self.key,
            'type': 'Page',
            'category': self.category,
            'parentId': None if self.group is None else self.group.pk,
            'permissions': [child.get_dict() for child in self.children.all()],
            'sort': self.sort

        }
        return item



