#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:Administrator
@file: urls.py
@time: 2020/02/{DAY}
"""
from django.urls import path
from . import views
from verifications.views import send_sms
app_name = 'users'

urlpatterns = [
    # path('', views.demo),
    path('', views.index),
    # path('Image_code/<id>', views.Image_code, name='Image_code'),
    # path('Image_code/<uuid:img_id>/', views.Image_code, name='Image_code'),
    path('register/', views.register, name='register'),


    # 方法一
    path('register/', views.RegisterView.as_view(), name='register'),
    # 方法二
    # path('register/', views.reg),


    path('login/', views.lo,name='login'),
    path('logout/', views.LogOut,name='logout'),
    path('c/', views.P,name='c'),
    path('send_sms/', send_sms),
    path('check/', views.check),



]
