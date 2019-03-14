#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
app_name = 'index'
from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # path('admin/', admin.site.urls),

    # path('', views.index.as_view())

    path('', TemplateView.as_view(template_name='index/index.html')),
    # path('square', TemplateView.as_view(template_name='index/square.html'), name='square')
    path('square', views.square, name='square'),
    path('test', views.test)
]

# 我一定能学会 我一定要好好学习 （自信满满）
# 还真有点难，我到底能不能学会 （自我怀疑）
# 咋还不毕业啊，这是啥老师啊，咋啥都不讲 （内心开始浮躁）【学习方法、学习习惯】
# 我擦，咋就毕业了呢，我还啥都不会呢 （内心开始恐慌）














