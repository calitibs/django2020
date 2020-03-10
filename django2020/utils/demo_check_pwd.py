#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:Administrator
@file: demo_check_pwd.py
@time: 2020/03/{DAY}
"""
import requests
import json

url = 'http://127.0.0.1:2222/user/check/'

r = requests.post(url, data=
{
    'telephone': 13536020880,
    'old_password': 123456,
    'new_password': 1234567
}
                  )
print(r.text)
