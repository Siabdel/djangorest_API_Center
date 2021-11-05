#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file
This program is appli todo for manage incidents and action
"""

__author__ = 'Abdelaziz Sadquaoui asadquaoui@strandcosmeticseurope.com'
__copyright__ = 'Copyright (c) 2019 strandcosmeticseurope.fr'
__version__ = '0.9'

from django.conf.urls import url, include
# API
from rest_framework.urlpatterns import format_suffix_patterns
from apibankpro import settings
from django.conf.urls.static import static
import datetime, os
from django.views.generic import TemplateView
from django.conf.urls import include, url
from rest_framework import routers
from django.contrib import admin
from django.conf import settings
from appipro import views as apiviews

urlpatterns =[
    # Projects home
    # users dispo
    url(r'^puser/(?P<user_id>[-\d]+)$', apiviews.MemberList.as_view()),
    url(r'^directories/$', apiviews.DirectoryList.as_view()),
    url(r'^todos/$', apiviews.TodoList.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ajout de sufixe au api url (.json, .api)
urlpatterns = format_suffix_patterns(urlpatterns)
