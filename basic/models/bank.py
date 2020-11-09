#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from config.models import Service
from config.models import ENV_STAGE
from config.models import Service

import logging, traceback
from collections import OrderedDict
logger = logging.getLogger(__name__)

class Bank(models.Model):
    """
    Bank
    """
    bank_name = models.CharField('BankName', max_length=50, default='Name')
    bank_code = models.CharField('BankCode', max_length=50, default='Code')
    description = models.CharField('Description', max_length=100, default='', blank=True)

    class Meta:
        app_label = 'basic'

    def get_dict(self):
        item = {
            'bank_name': self.bank_name,
            'bank_code': self.bank_code,
        }
        return item