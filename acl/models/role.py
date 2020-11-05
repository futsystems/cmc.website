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
from permission import Permission
from choices import PERMISSION_TYPE
from page import Page


class Role(models.Model):
    """
    Role
    """
    name = models.CharField('Name', max_length=50, default='Name')
    key = models.CharField('Key', max_length=100, default='', blank=True)

    permissions = models.ManyToManyField(Permission, verbose_name='Permissions', blank=True)
    description = models.CharField('Description', max_length=100, default='', blank=True)

    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    sort = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        app_label = 'acl'
        ordering = ['sort']


    def get_dict(self):
        item = {
            'pk': self.pk,
            'name': self.name,
            'key': self.key,
            'type': 'Role',
            'description': self.description,
            'permissionsPKs': [item.pk for item in self.permissions.all()],
            'sort': self.sort

        }
        return item