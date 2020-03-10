#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:Administrator
@file: qqdl.py
@time: 2020/03/{DAY}
"""
from django2020.QQLoginTool.QQtool import OAuthQQ

app_id = '101853453'
ak = '7b4d2f3ca899b12db236952b9818c497'
red_url = 'http://www.ccmsy.com:8000/auth_callback'
state = ''

# 鉴权
auth = OAuthQQ(
    client_id=app_id, client_secret=ak, redirect_uri=red_url, state=state
)

# 获取QQ登录地址
login_url = auth.get_qq_url()
print(login_url)
