#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Administrator
@file: QR.py
@time: 2020/03/{DAY}
"""

from MyQR import myqr as mq
# 生成普通二维码，生成的二维码路径与源代码路径一致
mq.run('https://www.baidu.com/',save_name='m.png')
print('生成的二维码路径与源代码路径一致')