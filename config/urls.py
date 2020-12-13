# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


import views

urlpatterns = [
    url(r'^gateway/$', views.gateway_config_ocelot, name='gateway_config_ocelot'),
    url(r'^gateway/hash/$', views.gateway_config_ocelot_hash, name='gateway_config_ocelot_hash'),
    url(r'^gateway/dotnet/$', views.gatwway_config_dotnet, name='gateway_config_dotnet'),
    url(r'^gateway/dotnet/hash/$', views.gatwway_config_dotnet_hash, name='gateway_config_dotnet_hash'),
    url(r'^service/list/$', views.service_list, name='config_services_list'),

    url(r'^service/$', views.service, name='service_config'),
    url(r'^service/hash/$', views.service_hash, name='service_config_hash'),

    url(r'^gitlab/notify/$', views.gitlab_event, name='gitlab_event_notify'),

    #url(r'^service/used/$', views.used_services, name='config_used_services'),
]