#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models


class RateLimitOption(models.Model):
    """
    rate limite option
    """
    name = models.CharField('RateLimitOption Name', max_length=50, default='Default')
    client_whitelist = models.CharField('ClientWhitelist', max_length=255, blank=True,  default='')
    enable_rate_limiting = models.BooleanField('EnableRateLimiting', default=True)
    period = models.CharField('Period', max_length=255, default='')
    period_timespan = models.IntegerField('PeriodTimespan', default=0)
    limit = models.IntegerField('Limit', default=0)

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'RateLimitOption-%s' % self.name

    def to_dict(self):
        dict = {
            'EnableRateLimiting':self.enable_rate_limiting,
            'Period':self.period,
            'PeriodTimespan':self.period_timespan,
            'Limit':self.limit,


        }
        if self.client_whitelist != '':
            dict['ClientWhitelist']= self.client_whitelist.split(',')

        return dict


