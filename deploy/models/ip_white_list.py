#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from config.models import Service, ApiGateway, Portal
from choices import LOCATION, NODETYPE
from config.models.choices import ENV_STAGE

class ServerManager(models.Manager):

    def in_white_list(self,ip):
        return self.filter(ip=ip).first() is not None


class IP(models.Model):
    """
    IP
    """
    name = models.CharField('Name', max_length=100, default='Node1', unique=True)
    ip = models.CharField('IP', max_length=50, default='127.0.0.1')
    is_blocked = models.BooleanField('Blocked', default=False)
