#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from choices import LOG_LEVEL_NET_CORE, ENV_STAGE


class ElastAPM(models.Model):
    """
    elastic apm config
    """
    default_service_name = models.CharField('Default Service Name', max_length=50, default='DefualtService')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    service_urls = models.CharField('Host', max_length=50, default='http://apm.marvelsystem.net:8200')
    log_level = models.CharField(verbose_name='LogLevel', max_length=20, choices=LOG_LEVEL_NET_CORE, default='Debug')
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'ElastAPM-%s' % self.service_urls

    def to_dict(self):
        dict = {
            'ServiceName': self.default_service_name,
            'LogoLevel': self.log_level,
            'ServerUrls': self.service_urls,
        }
        return dict
