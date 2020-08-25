# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


import views

urlpatterns = [
    url(r'^gateway/$', views.config_gateway, name='config_gateway'),
    url(r'^service/list/$', views.service_list, name='config_services_list'),

    url(r'^service/$', views.service, name='config_services'),
    url(r'^service/hash/$', views.service_hash, name='config_services_hash'),
]