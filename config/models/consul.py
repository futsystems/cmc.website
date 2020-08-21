#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from choices import ENV_STAGE

class Consul(models.Model):
    """
    consul node
    """
    name = models.CharField('Consul Name', max_length=50, default='Consul')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    host = models.CharField('host', max_length=50, default='test.marvelsystem.net')
    port = models.IntegerField('Port', default=8500)
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'consul-%s %s' % (self.name, self.env)

    def to_dict(self):
        dict = {
            'Host': self.host,
            'Port': self.port,
            'Type': 'Consul',
        }
        return dict

