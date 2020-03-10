#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:Administrator
@file: forms.py
@time: 2020/03/{DAY}
"""

from django import forms
import re
from django.contrib.auth import login
from django.db.models import Q
from . import constants

from .models import Users


class LoginForm(forms.Form):
    user_account = forms.CharField()
    # 重写错误
    password = forms.CharField(max_length=20, min_length=6, error_messages={
        'min_length': '密码长度大于6',
        'max_length': '密码长度小于20',
        'required': '密码不能为空'
    })
    remember = forms.BooleanField(required=False)

    # 因为forms.py里def post(self, request)传了request请求，需要重写
    def __init__(self, *a, **k):
        self.request = k.pop('request')  # 删除键
        super().__init__(*a, **k)  # 取值

    # clean_+验证名
    def clean_user_account(self):
        user_info = self.cleaned_data.get('user_account')
        if not user_info:
            raise forms.ValidationError('用户名不能为空')

        if not re.match(r'^1[3-9]\d{9}$]', user_info) and (len(user_info) < 5 or len(user_info) > 20):
            raise forms.ValidationError('输入的用户名格式错误，请重新输入')
        return user_info

    def clean(self):
        cleaned_data = super().clean()
        user_info = cleaned_data.get('user_account')
        pass_wd = cleaned_data.get('password')
        rmber = cleaned_data['remember']

        # 判断是否是用户名还是手机号   Q
        user_qs = Users.objects.filter(Q(mobile=user_info) | Q(username=user_info))

        if user_qs:
            user = user_qs.first()
            # 判断密码
            if user.check_password(pass_wd):
                if rmber:
                    # 设置密码保存时间 None 默认14天(60*60*24*7*2)
                    # self.request.session.set_expiry(None)
                    self.request.session.set_expiry(constants.SESSION_EXPIRY_TIME)
                else:
                    # 一次性登录
                    self.request.session.set_expiry(constants.SESSION_TIME)
                login(self.request, user)
            else:
                raise forms.ValidationError('用户名或密码错误，请重新输入')

        else:
            raise forms.ValidationError('用户名不存在，请重新输入')
        return cleaned_data
