#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from choices import LOG_LEVEL_NET_CORE, ENV_STAGE

class LogItem(models.Model):
    """
    log item
    """
    prefix = models.CharField('Prefix', max_length=100, default='Microsoft')
    level = models.CharField(max_length=20, choices=LOG_LEVEL_NET_CORE, default='Information')

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'%s:%s' % (self.prefix, self.level)

class LogItemGroup(models.Model):
    name = models.CharField('Name', max_length=100, default='Default')
    items = models.ManyToManyField(LogItem, verbose_name='Log Items')
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'log-%s' % self.name

    def to_dict(self):
        level_data = {}
        for item in self.items.all():
            level_data[item.prefix] = item.level

        dict = {
            'LogLevel': level_data
        }
        return dict
