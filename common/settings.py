#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
gettext = lambda s: s


GITLAB_SETTING= getattr(settings, 'GITLAB_SETTING', None)


