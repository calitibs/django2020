#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:Administrator
@file: demo_login.py
@time: 2020/03/{DAY}
"""
import requests
import json

url = 'http://127.0.0.1:2222/user/login/'
# json.dumps
r = requests.post(url, data=json.dumps(
    {
        'user_account': 'lilili',
        'password': 123456,
        'remember': False

    }
))
print(r.text)
