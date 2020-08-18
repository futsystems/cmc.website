#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models


class HeaderTransform(models.Model):
    """
    Header Transform
    """
    name = models.CharField('Name', max_length=50, default='HeaderTrannsform')
    header_key = models.CharField('HeaderKey', max_length=50, default='X-Forwarded-For')
    header_value = models.CharField('HeaderValue', max_length=50, default='{RemoteIpAddress}')
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'HeaderTransform-%s' % self.header_key