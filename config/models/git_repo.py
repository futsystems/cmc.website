#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from service import Service
from choices import NODETYPE

class GitLabProject(models.Model):
    """
    GitProject
    """
    path = models.CharField('Path', max_length=100, default='platform/path', unique=True)
    node_type = models.CharField("Node Type", max_length=20, choices=NODETYPE, default='Service')
    node_name = models.CharField("Node Name", max_length=20, default='APIGateway')

    project_id = models.CharField(max_length=5, default='1')
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'%s-%s' % (self.path, self.project_id)

    @property
    def pipeline_status_image(self):
        return ["https://gitlab.marvelsystem.net/%s/badges/develop/pipeline.svg" % self.path,
                "https://gitlab.marvelsystem.net/%s/badges/master/pipeline.svg" % self.path]

    def on_pipeline_success(self,tag):
        try:
            tag_info = self.tags.filter(tag=tag)
        except Exception:
            tag_info = TagInfo()
            tag_info.project = self

        tag_info.tag = tag
        tag_info.version = tag[1:]
        tag_info.db_version = 0
        tag_info.save()



class TagInfo(models.Model):
    """
    TagInfo
    """

    class NodeName(object):

        @classmethod
        def get_node_name_choices(cls):
            result = [(item.name, 'Service_%s' % item.name) for item in
                      Service.objects.filter(env='Development').order_by('name').all()]
            result.append(('APIGateway', 'Gateway_APIGateway'))
            result.append(('Admin', 'Portal_Admin'))
            result.append(('Console', 'Portal_Console'))
            result.append(('H5', 'Portal_H5'))
            return tuple(result)

    project = models.ForeignKey(GitLabProject, verbose_name='Git Project', related_name='tags')
    #node_type = models.CharField("Node Type", max_length=20, choices=NODETYPE, default='Service')
    #node_name = models.CharField("Node Name", max_length=20, choices=NodeName.get_node_name_choices(),
    #                             default='APIGateway')
    tag = models.CharField('Tag', max_length=50, default='v1.0.0')
    version = models.CharField('Image Version', max_length=50, default='1.0.0')
    db_version = models.CharField('DB Version', max_length=50, default='20200101180500')#年月日时分秒代表数据库版本号

    def __unicode__(self):
        return u'%s-%s' % (self.project, self.tag)