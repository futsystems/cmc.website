#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from config.models import Service
from choices import LOCATION


class ServiceNode(models.Model):
    """
    server
    """
    name = models.CharField('Name', max_length=100, default='Node1')
    location = models.CharField(max_length=20, choices=LOCATION, default='hangzhou')
    ip = models.CharField('IP', max_length=50, default='127.0.0.1')
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'%s:%s' % (self.prefix, self.level)