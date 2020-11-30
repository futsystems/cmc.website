#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from config.models import Service, ApiGateway, Portal
from choices import LOCATION, NODETYPE, PRODUCTTYPE
from config.models.choices import ENV_STAGE



class Deploy(models.Model):
    """
    Deploy
    """
    name = models.CharField('Name', max_length=100, default='DeployName', unique=True)
    product_type = models.CharField(max_length=20, choices=PRODUCTTYPE, default='WeiShop')
    location = models.CharField(max_length=20, choices=LOCATION, default='hangzhou')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    suffix = models.CharField('Suffix', max_length=100, default='suffix', unique=True)


    class Meta:
        app_label = 'deploy'

    def __unicode__(self):
        return u'%s-%s' % (self.product_type, self.suffix)


