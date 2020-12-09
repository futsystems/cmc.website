#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models

class GitLabProject(models.Model):
    """
    GitProject
    """
    path = models.CharField('Path', max_length=100, default='platform/path', unique=True)
    project_id = models.CharField(max_length=5, default='1')
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'%s-%s' % (self.path, self.project_id)