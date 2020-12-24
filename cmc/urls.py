"""ms_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from config import urls as config_urls
from deploy import urls as deploy_urls
from acl import urls as acl_urls
from basic import urls as basic_urls
from update import urls as update_urls
from feed import urls as feed_urls

#from adminplus.sites import AdminSitePlus
#admin.site = AdminSitePlus()
#admin.autodiscover()

urlpatterns = [
    url(r'^config/', include(config_urls)),
    url(r'^deploy/', include(deploy_urls)),
    url(r'^acl/', include(acl_urls)),
    url(r'^basic/', include(basic_urls)),
    url(r'^update/', include(update_urls)),
    url(r'^feed/', include(feed_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
]


urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()