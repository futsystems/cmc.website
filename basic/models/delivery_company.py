#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from config.models import Service
from config.models import ENV_STAGE
from config.models import Service

import logging, traceback
from collections import OrderedDict
logger = logging.getLogger(__name__)

class DeliveryCompany(models.Model):
    """
    DeliveryCompany
    """
    company_name = models.CharField('CompanyName', max_length=50, default='Name')
    company_code = models.CharField('CompanyCode', max_length=50, default='Code')
    description = models.CharField('Description', max_length=100, default='', blank=True)

    class Meta:
        app_label = 'basic'

    def get_dict(self):
        item = {
            'company_name': self.company_name,
            'company_code': self.company_code,
        }
        return item