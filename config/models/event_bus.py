#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from choices import LOG_LEVEL_NET_CORE,ENV_STAGE


class EventBus(models.Model):
    """
    eventbus apm config
    """
    default_subscription_client_name=models.CharField('ClientName', max_length=50, default='SubscriptionClientName')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    retry_count = models.IntegerField('Retry Count', default=5)
    host = models.CharField('Host', max_length=50, default='test.marvelsystem.net')
    user_name= models.CharField('UserName', max_length=50, default='user')
    password = models.CharField('Password', max_length=50, default='user')
    description = models.CharField('Description', max_length=1000, default='', blank=True)


    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'EventBus-%s' % self.host

    def to_dict(self):
        dict = {
            "SubscriptionClientName": self.default_subscription_client_name,
            'EventBusRetryCount': self.retry_count,
            'EventBusConnection': self.host,
            'EventBusUserName': self.host,
            'EventBusPassword': self.host,
        }
        return dict
