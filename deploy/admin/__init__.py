#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from .. import models
from server import ServerAdmin
from deploy import DeployAdmin
from ip import IPAdmin
from version import VersionAdmin
from wx_miniprograme_template import WeiXinMiniprogramTemplateAdmin


admin.site.register(models.Server, ServerAdmin)
admin.site.register(models.Deploy, DeployAdmin)
admin.site.register(models.IP, IPAdmin)
admin.site.register(models.Version, VersionAdmin)
admin.site.register(models.WeiXinMiniprogramTemplate, WeiXinMiniprogramTemplateAdmin)
