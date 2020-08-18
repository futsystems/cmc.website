#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models


class HttpHandlerOption(models.Model):
    """
    http handler option
    """
    name = models.CharField('HttpHandlerOption Name', max_length=50, default='Default')
    allow_auto_redirect = models.BooleanField('AllowAutoRedirect', default=True)
    use_cookie_container = models.BooleanField('UseCookieContainer', default=True)
    user_tracing = models.BooleanField('UseTracing', default=True)
    max_connections_per_server = models.IntegerField('MaxConnectionsPerServer', default=500)

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'HttpHandlerOption-%s' % self.name

    def to_dict(self):
        dict = {
            'AllowAutoRedirect':self.allow_auto_redirect,
            'UseCookieContainer':self.use_cookie_container,
            'UseTracing':self.user_tracing,
            'MaxConnectionsPerServer':self.max_connections_per_server,
        }
        return  dict

