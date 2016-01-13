'''cs URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
'''
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from views import *

urlpatterns = [
    url(r'^$', populate_home_page),
    url(r'^search/$', populate_search),
    url(r'^aboutus/$', populate_about_us),
    url(r'^static/(.*)', return_static_file),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/cs/images/favicon.ico')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(.*)', handler404),
]