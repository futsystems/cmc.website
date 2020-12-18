#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
import django.utils.timezone as timezone
from choices import LOCATION, NODETYPE, PRODUCTTYPE
from config.models.choices import ENV_STAGE
from config.models import Consul
from deploy import Deploy
from choices import NODETTYPE
from config.models import Service, TagInfo, GitLabProject
import json


class Version(models.Model):
    """
    Version, set software version
    """

    class NodeName(object):

        @classmethod
        def get_node_name_choices(cls):
            result = [(item.name, 'Service_%s' % item.name) for item in Service.objects.filter(env='Development').order_by('name').all()]
            result.append(('APIGateway', 'Gateway_APIGateway'))
            result.append(('Admin', 'Portal_Admin'))
            result.append(('Console', 'Portal_Console'))
            result.append(('H5', 'Portal_H5'))
            return tuple(result)

    deploy = models.ForeignKey(Deploy, verbose_name='Deploy', on_delete=models.SET_NULL, default=None,
                                blank=True, null=True, related_name='versions')
    project = models.ForeignKey(GitLabProject, verbose_name='Project', on_delete=models.SET_NULL, default=None,
                               blank=True, null=True, related_name='versions')

    tag = models.ForeignKey(TagInfo, verbose_name='Tag', on_delete=models.SET_NULL, default=None,
                                blank=True, null=True, related_name='versions')

    apm_sample = models.BooleanField('APM Sample', default=False)

    class Meta:
        app_label = 'deploy'

    def __unicode__(self):
        return u'%s-%s' % (self.deploy, self.tag)

    @property
    def tag_name(self):
        if self.tag is None:
            return 'None'
        else:
            return self.tag.tag




