#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:Administrator
@file: tasks.py
@time: 2020/03/{DAY}
"""
# 在celery_tasks目录下创建sms目录，用于放置发送短信的异步任务相关代码。

# 在celery_tasks/sms/目录下创建tasks.py文件，用于保存发送短信的异步任务

#  实现异步处理短信
from celery_tasks.main import celery_app
from django2020.utils.yuntongxun.sms import CCP
# bind
# retry_backoff   间隔时间
from users.views import logger


@celery_app.task(bind=True, name='send_sms_code', retry_backoff=3)
def send_sms_code(self, mobile, sms_code):
    """
    手机号
    短信验证码
    :param self:
    :param mobile:
    :param sms_code:
    :return:
    """
    try:
        send_res = CCP().send_template_sms(mobile, [sms_code, 5], 1)
    except Exception as e:
        logger.error(e)
        # 有异常触发3次
        raise self.retry(exc=e, max_retries=3)
    if send_res != 0:
        raise self.retry(exc=Exception('发送短信失败'), max_retries=3)
    return send_res
