# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


import views

urlpatterns = [
    url(r'^permission/sync/$', views.sync_permission, name='permission_sync'),
    url(r'^permission/$', views.permission, name='permission_sync'),

]