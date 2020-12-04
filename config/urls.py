# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


import views

urlpatterns = [
    url(r'^gateway/$', views.config_gateway, name='config_gateway_ocelot'),
    url(r'^gateway/hash/$', views.config_gateway_hash, name='config_gateway_ocelot_hash'),
    url(r'^gateway/dotnet/$', views.gatwway_config_dotnet, name='gateway_config_dotnet'),
    url(r'^gateway/dotnet/hash/$', views.gatwway_config_dotnet_hash, name='gateway_config_dotnet_hash'),
    url(r'^service/list/$', views.service_list, name='config_services_list'),

    url(r'^service/$', views.service, name='config_service'),
    url(r'^service/hash/$', views.service_hash, name='config_service_hash'),

    #url(r'^service/used/$', views.used_services, name='config_used_services'),
]