#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:Administrator
@file: urls.py
@time: 2020/02/{DAY}
"""

from django.urls import path, re_path
from . import views
from users.views import s

urlpatterns = [
    path('', s), # 调用方法
    # path('Image_code/<uuid:img_id>/', views.Image_code, name='Image_code'),
    path('image_code/<uuid:image_code_id>/', views.ImageCode.as_view(), name='image_code'),
    re_path('username/(?P<username>\w{5,20})/', views.CheckUsernameView.as_view(), name='CheckUsernameView'),
    # re_path('mobile/(?P<mobile>1[3-9]\d{9})/', views.CheckMobileView.as_view(), name='CheckMobileView'),
    re_path('mobiles/(?P<mobile>1[3-9]\d{9})/', views.CheckMobileView.as_view(), name='mobile'),
    path('sms_code/', views.SmsCodeView.as_view(), name='sms_code'),
]
