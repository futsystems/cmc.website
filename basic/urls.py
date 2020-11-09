# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


import views

urlpatterns = [
    url(r'^bank/$', views.bank, name='bank'),
    url(r'^delivery_company/$', views.delivery_company, name='delivery_company'),
    url(r'^region/$', views.region, name='region'),
]