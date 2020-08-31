#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from choices import ENV_STAGE

class WXBoundServer(models.Model):
    """
    微信边界服务器，微信接口调用需要将调用服务器加入白名单
    """
    name = models.CharField('Consul Name', max_length=50, default='node-01')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    ip = models.CharField('IP', max_length=50, default='127.0.0.1')
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'WX-%s %s' % (self.name, self.env)

