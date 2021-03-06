# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


import views

urlpatterns = [
    url(r'^node/up/$', views.register_node_info, name='node_up'),
    url(r'^node/down/$', views.unregister_node_info, name='node_down'),
    url(r'^node/health/$', views.update_health_info, name='update_node_health_info'),

    url(r'^info/$', views.node_info, name='deploy_info'),

    url(r'^server/pillar/$', views.salt_pillar, name='server_pillar'),
    url(r'^minion/valid/(?P<minion_id>[a-zA-Z0-9_.-]+)', views.minion_valid,
        name='server_minion_valid'),
]