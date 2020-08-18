# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import views

urlpatterns = patterns('',

    url(r'^gateway/$',views.config_gateway, name='config_gateway'),
)