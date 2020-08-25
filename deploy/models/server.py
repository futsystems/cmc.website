#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from config.models import Service
from choices import LOCATION
from config.models.choices import ENV_STAGE



class Server(models.Model):
    """
    server
    """
    name = models.CharField('Name', max_length=100, default='Node1')
    location = models.CharField(max_length=20, choices=LOCATION, default='hangzhou')
    ip = models.CharField('IP', max_length=50, default='127.0.0.1')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    installed_services = models.ManyToManyField(Service, verbose_name='Installed Services', blank=True)

    description = models.CharField('Description', max_length=1000, default='', blank=True)



    class Meta:
        app_label = 'deploy'

    def __unicode__(self):
        return u'%s-%s' % (self.name, self.ip)

    def get_pillar(self):
        data = {
            'name': self.name,
            'ip': self.ip,
            'env': self.env,
            'services':[item.get_pillar() for item in self.installed_services.all()]
        }
        return data

