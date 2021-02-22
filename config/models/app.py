#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from choices import ENV_STAGE
from common import GitlabAPI


class AppH5(models.Model):
    """
    后台网站终端
    """
    name = models.CharField('Portal Name', max_length=50, default='Portal')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')

    description = models.CharField('Description', max_length=1000, default='', blank=True)

    merge_success = models.BooleanField('Merge Success', default=True)
    merge_message = models.CharField('Merge Message', max_length=500, default='', blank=True, null=True)

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'app-%s' % self.env

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
            'domain_name': deploy.app_domain_name,
            'api_gw_domain': deploy.gateway_domain_name
        }

        if deploy.env == 'Development':
            dict['branch'] = 'develop'
        elif deploy.env == 'Staging':
            dict['branch'] = 'master'
        else:
            dict['branch'] = 'master'


        #if self.env == 'Production':
        #    dict['admin_tag'] = deploy.get_version('Portal', 'Admin')
        #    dict['console_tag'] = deploy.get_version('Portal', 'Console')
        #    dict['h5_tag'] = deploy.get_version('Portal', 'H5')


        return dict
