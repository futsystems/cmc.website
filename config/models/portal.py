#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from choices import ENV_STAGE
from common import GitlabAPI


class Portal(models.Model):
    """
    后台网站终端
    """
    name = models.CharField('Portal Name', max_length=50, default='Portal')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')

    admin_pipeline_trigger = models.CharField('Admin Pipeline Trigger', max_length=1000, default='', blank=True)
    console_pipeline_trigger = models.CharField('Console Pipeline Trigger', max_length=1000, default='', blank=True)
    h5_pipeline_trigger = models.CharField('H5 Pipeline Trigger', max_length=1000, default='', blank=True)

    description = models.CharField('Description', max_length=1000, default='', blank=True)

    merge_success = models.BooleanField('Merge Success', default=True)
    merge_message = models.CharField('Merge Message', max_length=500, default='', blank=True, null=True)

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'portal-%s' % self.env

    def merge_project(self):
        import time
        if self.env == 'Development':
            api = GitlabAPI()
            path1 = 'terminal-portal/admin'
            ret1 = api.merge_project(path1)

            path2 = 'terminal-portal/console'
            ret2 = api.merge_project(path2)

            path3 = 'terminal-portal/h5'
            ret3 = api.merge_project(path3)

            self.merge_success = ret1[0] and ret2[0] and ret3[0]
            self.merge_message ='%s,%s,%s' % (ret1[1], ret2[1], ret3[1])
            self.save()
        else:
            self.merge_success = True
            self.merge_message = 'Only Development Merge'

    def get_pillar(self, deploy):
        dict = {
            'domain_name': deploy.portal_domain_name,
            'partion_info_api_domain': deploy.website_domain_name,
            'api_gw_domain': deploy.gateway_domain_name
        }

        if self.env == 'Production':
            dict['admin_tag'] = deploy.portal_admin_tag
            dict['console_tag'] = deploy.portal_console_tag
            dict['h5_tag'] = deploy.portal_h5_tag
        else:
            dict['admin_tag'] = self.env
            dict['console_tag'] = self.env
            dict['h5_tag'] = self.env

            dict['admin_pipeline_trigger'] = self.admin_pipeline_trigger
            dict['console_pipeline_trigger'] = self.console_pipeline_trigger
            dict['h5_pipeline_trigger'] = self.h5_pipeline_trigger

        return dict
