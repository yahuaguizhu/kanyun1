#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
app_name = 'user'

from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [

    path('login', views.login.as_view(), name='login'),

    path('register', views.register.as_view(), name='register'),

    path('doc_lists', views.doc_list, name='user_doc_lists'),
    path('doc_lists/<int:page>', views.doc_list, name='user_doc_lists'),

    path('create_content/<int:id>/<int:cid>', views.create_content.as_view(), name='create_content'),


    path('sendsms', views.send_sms, name='sendsms'),
    path('logout', views.logout, name='logout'),

    path('create_chapter', views.create_chapter, name='create_chapter'),

    path('create_chapter_form/<int:id>/<int:cid>', views.create_chapter_form, name='create_chapter_form'),
    path('add_content', views.add_content, name='add_content'),

    path('book_set/<id>', views.book_set.as_view(), name='book_set'),

    path('add_book_tag', views.add_book_tag, name='add_book_tag'),
    path('delete_book_tag', views.delete_book_tag, name='delete_book_tag'),
    path('upload_avatar', views.upload_avatar, name='upload_avatar'),
    path('modify', views.modify.as_view(), name='modify'),


]
















