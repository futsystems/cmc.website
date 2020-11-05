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
    __original_key = None

    def __init__(self, *args, **kwargs):
        super(Group, self).__init__(*args, **kwargs)
        self.__original_key = self.name

    title = models.CharField('Title', max_length=50, default='Title')
    name = models.CharField('Name', max_length=50, default='Name')
    icon = models.CharField('Icon', max_length=50, default='Icon')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    description = models.CharField('Description', max_length=100, default='', blank=True)
    sort = models.PositiveIntegerField(default=0, blank=False, null=False)


    class Meta:
        app_label = 'acl'
        ordering = ['sort']

    def __unicode__(self):
        return u'%s[%s]' % (self.title, self.name)


    def save(self, *args, **kwargs):
        super(Group, self).save(*args, **kwargs)

        # key changed then save all children
        if self.name != self.__original_key:
            for item in self.children.all():
                item.save()
        self.__original_key = self.name

    def get_dict(self):
        item = {
            'pk': self.pk,
            'title': self.title,
            'icon': self.icon,
            'name': self.name,
            'key': self.name,
            'type': 'Group',
            'pages': [child.get_dict() for child in self.children.all()],
            'sort': self.sort

        }
        return item