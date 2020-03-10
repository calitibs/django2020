#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:Administrator
@file: main.py
@time: 2020/03/{DAY}
"""
# 在celery_tasks目录下创建main.py文件，用于作为celery的启动文件
from celery import Celery

import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE']='django2020.settings.dev'
# 创建实例
celery_app = Celery('sms_code')

# 加载配置
celery_app.config_from_object('celery_tasks.config')

# 注册任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])
