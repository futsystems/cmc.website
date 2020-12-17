#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from eventbus import EventBublisher, CMCMiniprogramRelease
import requests


class WeiXinMiniprogramTemplate(models.Model):
    """
    WeiXinMiniprogramTemplate
    """
    name = models.CharField('Name', max_length=100, default='App', unique=True)
    app_id = models.CharField(max_length=20, default='wx000000000000', unique=True)
    web_hook = models.CharField(max_length=255, default='')
    description = models.CharField('Description', max_length=1000, default='', blank=True)
    latest_version = models.CharField(max_length=255, default='')

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'%s-%s' % (self.name, self.app_id)

    def release(self):

        result = requests.post(self.web_hook).json()
        if result['code'] == 0:
            self.latest_version = result['data']
            self.save()
            self.publish_release_event(self.latest_version)
        return result

    def publish_release_event(self, version):
        for deploy in self.deploys.all():
            ev = CMCMiniprogramRelease(deploy.key, 'WeiXinMini', version)
            if deploy.event_bus is not None:
                EventBublisher(deploy.event_bus).send_message(ev)

