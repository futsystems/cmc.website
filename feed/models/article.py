#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from choices import ARTICLE_TYPE
import django.utils.timezone as timezone


class Article(models.Model):
    """
    article
    """
    title = models.CharField('Title', max_length=100, default='Title')
    type = models.CharField(max_length=20, choices=ARTICLE_TYPE, default='Doc')
    url = models.CharField('Url', max_length=255, default='https://www.marvelsystem.net')
    description = models.CharField('Description', max_length=1000, default='', blank=True)
    create_time = models.DateTimeField('DateTime', default=timezone.now)

    class Meta:
        app_label = 'feed'

    def __unicode__(self):
        return u'article-%s' % self.title

    def to_dict(self):
        dict = {
            'title': self.title,
            'type': self.type,
            'url': self.url,
        }
        return dict

