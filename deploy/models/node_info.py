#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models
import django.utils.timezone as timezone
from choices import LOCATION, NODETYPE, PRODUCTTYPE
from config.models.choices import ENV_STAGE
from config.models import Consul
from deploy import Deploy
import json

import logging, traceback
logger = logging.getLogger(__name__)


class NodeInfo(models.Model):
    """
    NodeInfo, node report information to CMC
    """
    deploy = models.ForeignKey(Deploy, verbose_name='Consul', on_delete=models.SET_NULL, default=None,
                                blank=True, null=True, related_name='nodes')

    node_type = models.CharField(max_length=20, default='Portal')
    node_name = models.CharField(max_length=20, default='Gateway')
    ip = models.CharField('IP', max_length=50, default='127.0.0.1')

    product_type = models.CharField(max_length=20, choices=PRODUCTTYPE, default='WeiShop')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')

    version = models.CharField('Version', max_length=100, default='1.0.0')
    framework = models.TextField('Framework', default='{}')

    health_report = models.TextField('Health Report', default='{}')

    up = models.BooleanField('No Up', default=False)
    up_time = models.DateTimeField('Up Time', default=timezone.now)
    last_active_time = models.DateTimeField('Last Active Time', auto_now=True)

    class Meta:
        app_label = 'deploy'

    def __unicode__(self):
        return u'%s-%s' % (self.deploy, self.node_service)

    def to_dict(self):
        dict = {
            'id': self.pk,
            'name': self.node_name,
            "service": self.node_name,
            'ip': self.ip,
            'product': self.product_type,
            'env': self.env,
            'version': self.version,
            'framework': json.loads(self.framework),
            'framework_version': '',
            'health': json.loads(self.health_report),
            'up': self.up,
            'up_time': self.up_time.strftime("%Y-%m-%d %H:%M:%S"),
            'last_active_time': self.last_active_time.strftime("%Y-%m-%d %H:%M:%S")
        }

        #logger.info(self.last_active_time)

        for dll in dict['framework']:
            if dll['name'] == 'Marvel.Web.Framework':
                dict['framework_version'] = dll['version']
        if dict['up'] is False:
            dict['health'] = {
                'status': 'Unhealthy',
                'entries': [],
                'description': 'service is not up, default status is Unhealthy',
            }
        return dict
