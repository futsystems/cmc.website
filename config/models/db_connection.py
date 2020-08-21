#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from choices import MYSQL_CHARSET, ENV_STAGE


class MySqlConnection(models.Model):
    """
    mysql connection info
    """
    name = models.CharField('DB Connection Name', max_length=50, default='Default')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    host = models.CharField('Host', max_length=50, default='test.marvelsystem.net')
    port = models.IntegerField('Port', default=8500)
    user = models.CharField('User', max_length=50, default='user')
    password = models.CharField('Password', max_length=50, default='password')
    database = models.CharField('Database', max_length=50, default='platform')
    charset = models.CharField(max_length=20, choices=MYSQL_CHARSET, default='utf8mb4')
    is_tracer = models.BooleanField('Is Tracer', default=True)
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'db-%s %s' % (self.name, self.env)

    def to_dict(self):
        dict = {
            'ConnectionName':self.name,
            'Host': 'server=%s;port=%s;uid=%s;pwd=%s;database=%s;charset=%s' % (self.host, self.port, self.user, self.password, self.database, self.charset),
            'DBProvider': 'MySql.Data.MySqlClient',
            'IsTracer': self.is_tracer
        }
        return dict
