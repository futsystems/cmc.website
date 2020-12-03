#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from config.models import Service, ApiGateway, Portal
from choices import LOCATION, NODETYPE, PRODUCTTYPE
from config.models.choices import ENV_STAGE
from config.models import Consul


class Deploy(models.Model):
    """
    Deploy
    """
    name = models.CharField('Name', max_length=100, default='DeployName', unique=True)
    product_type = models.CharField(max_length=20, choices=PRODUCTTYPE, default='WeiShop')
    location = models.CharField(max_length=20, choices=LOCATION, default='hangzhou')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    suffix = models.CharField('Suffix', max_length=100, default='suffix', unique=True)

    service_provider = models.ForeignKey(Consul, verbose_name='Consul', on_delete=models.SET_NULL, default=None,
                                         blank=True, null=True)

    key = models.CharField('Key', max_length=100, default='', blank=True)

    class Meta:
        app_label = 'deploy'

    def __unicode__(self):
        return u'%s-%s' % (self.product_type, self.suffix)

    def get_key(self):
        return '%s-%s' % (self.product_type, self.suffix)

    def save(self, *args, **kwargs):
        self.key = self.get_key()
        super(Deploy, self).save(*args, **kwargs)


