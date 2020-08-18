#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models


class HttpMethod(models.Model):
    """
    Http Method
    """
    name = models.CharField('Name', max_length=50, default='Get')
    method = models.CharField('Method', max_length=50, default='Get')

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'HttpMethod-%s' % (self.name)