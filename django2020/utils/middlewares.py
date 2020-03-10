#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Administrator
@file: middlewares.py
@time: 2020/03/{DAY}
"""

from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import get_token
class Middleware(MiddlewareMixin):
    def process_request(self,request):
        get_token(request)