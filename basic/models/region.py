#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from config.models import Service
from config.models import ENV_STAGE
from config.models import Service

import logging, traceback
from collections import OrderedDict
logger = logging.getLogger(__name__)

class Region(models.Model):
    """
    DeliveryCompany
    """
    region_name = models.CharField('RegionName', max_length=50, default='Name')
    region_code = models.CharField('RegionCode', max_length=50, default='Code')
    parent = models.ForeignKey('Region', verbose_name='Parent', related_name='children',
                              on_delete=models.SET_NULL, default=None, blank=True, null=True)
    description = models.CharField('Description', max_length=100, default='', blank=True)

    class Meta:
        app_label = 'basic'

    def __unicode__(self):
        return u'%s[%s]' % (self.region_name, self.region_code)

    def get_dict(self):
        item = {
            'region_name': self.region_name,
            'region_code': self.region_code,
            'parent_code': self.parent.region_code if self.parent is not None else None
        }
        return item