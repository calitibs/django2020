#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:Administrator
@file: demo.py
@time: 2020/03/{DAY}

"""
# 测试注册
import requests
import json

url = 'http://127.0.0.1:8000/user/register/'
# json.dumps
r = requests.post(url, data=json.dumps(
    {
        'username': 'lili123',
        'password': 123456
    }
))
print(r.text)
