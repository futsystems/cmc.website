#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from .. import models
from server import ServerAdmin
from deploy import DeployAdmin
from ip import IPAdmin

admin.site.register(models.Server, ServerAdmin)
admin.site.register(models.Deploy, DeployAdmin)
admin.site.register(models.IP, IPAdmin)
