#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from choices import ENV_STAGE


class Portal(models.Model):
    """
    后台网站终端
    """
    name = models.CharField('Portal Name', max_length=50, default='Portal')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    domain_name = models.CharField('Domain Name', max_length=100, default='dev-portal.marvelsystem.net')
    admin_pipeline_trigger = models.CharField('Admin Pipeline Trigger', max_length=1000, default='', blank=True)
    console_pipeline_trigger = models.CharField('console Pipeline Trigger', max_length=1000, default='', blank=True)
    description = models.CharField('Description', max_length=1000, default='', blank=True)


    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'portal-%s %s' % (self.domain_name, self.env)

    def get_pillar(self):
        dict = {
            "admin_pipeline_trigger": self.admin_pipeline_trigger,
            'console_pipeline_trigger': self.console_pipeline_trigger,
            'domain_name': self.domain_name,
        }
        return dict
