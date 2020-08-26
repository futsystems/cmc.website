#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from config.models import Service, ApiGateway
from choices import LOCATION, NODETYPE
from config.models.choices import ENV_STAGE

class ServerManager(models.Manager):

    def in_white_list(self,ip):
        return self.filter(ip=ip).first() is not None


class Server(models.Model):
    """
    server
    """
    name = models.CharField('Name', max_length=100, default='Node1')
    location = models.CharField(max_length=20, choices=LOCATION, default='hangzhou')
    ip = models.CharField('IP', max_length=50, default='127.0.0.1')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    node_type = models.CharField(max_length=20, choices=NODETYPE, default='Service')
    installed_services = models.ManyToManyField(Service, verbose_name='Installed Services', blank=True)

    gateway = models.ForeignKey(ApiGateway, verbose_name='Gateway', on_delete=models.SET_NULL, default=None,
                                         blank=True, null=True)

    description = models.CharField('Description', max_length=1000, default='', blank=True)

    objects = ServerManager()

    class Meta:
        app_label = 'deploy'

    def __unicode__(self):
        return u'%s-%s' % (self.name, self.ip)



    def get_pillar(self):
        data = {
            'name': self.name,
            'ip': self.ip,
            'env': self.env,
            'node_type': self.node_type,
        }
        if self.node_type == 'Service':
            data['services'] = [item.get_pillar() for item in self.installed_services.all()]
        if self.node_type == 'Gateway':
            data['gateway'] = None if self.gateway is None else self.gateway.get_pillar()
        return data

