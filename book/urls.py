#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
app_name = 'book'
from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('detail/<int:id>', TemplateView.as_view(template_name='book/detail.html'), name='detail'),
    path('content/<int:id>', TemplateView.as_view(template_name='book/content.html'), name='content'),
    # path('create', TemplateView.as_view(template_name='book/create.html'), name='create')
    path('create', views.create, name='create')
]
















