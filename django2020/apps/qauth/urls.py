#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:Administrator
@file: urls.py
@time: 2020/03/{DAY}
"""
from django.urls import path
from . import views

urlpatterns = [
    path('qq/login/', views.QQAuthView.as_view()),
    path('auth_callback/', views.auth_callback)

]
