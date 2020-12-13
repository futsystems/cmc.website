# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


import views

urlpatterns = [
    url(r'^diff/$', views.diff, name='diff'),
    url(r'^acl/diff/$', views.acl_diff, name='acl_diff'),
    #url(r'^demo/$', views.demo, name='demo'),
    #url(r'^demo2/$', views.demo2, name='demo2'),
]