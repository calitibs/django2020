import random
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from celery_tasks.sms.tasks import send_sms_code
from django2020.utils.captcha.captcha import captcha
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django_redis import get_redis_connection

import logging

from django2020.utils.yuntongxun.sms import CCP

logger = logging.getLogger('django')

from django.views import View
from users.models import Users
from django2020.utils.response_code import res_json, Code, error_map
import json


# 图形验证
# def Image_code(request, img_id):
#     text, image = captcha.generate_captcha()
#     redis_conn = get_redis_connection('verify_code')  # 连接数据库
#     # 保存id键 60存在时间 text值
#     redis_conn.setex('img_{}'.format(img_id).encode('utf8'), 60, text)
#     logger.info('图形验证码是：{}'.format(text))
#
#     # 设置过期时间
#     # request.session['image_code'] = text
#     # request.session.set_expiry(60)
#     # print(request.session.keys())
#     # print(111, request.session.get('image_code'))
#
#     return HttpResponse(content=image, content_type='image/jpg')
class ImageCode(View):
    """
    define image verification view
    # /image_codes/<uuid:image_code_id>/
    """
    def get(self, request, image_code_id):
        text, image = captcha.generate_captcha()
        # 确保settings.py文件中有配置redis CACHE
        # Redis原生指令参考 http://redisdoc.com/index.html
        # Redis python客户端 方法参考 http://redis-py.readthedocs.io/en/latest/#indices-and-tables
        con_redis = get_redis_connection(alias='verify_code')
        img_key = "img_{}".format(image_code_id).encode('utf-8')
        # 将图片验证码的key和验证码文本保存到redis中，并设置过期时间
        con_redis.setex(img_key,300, text)
        logger.info("Image code: {}".format(text))
        # HttpResponse(content=响应体, content_type=响应体数据类型, status=状态码)
        return HttpResponse(content=image, content_type="image/jpg")

# 用户名验证
class CheckUsernameView(View):
    """
    # 验证用户名
    route:username/(?P<username>\w{5,20})/
    :param username
    """

    def get(self, request, username):
        """
        统计数量，如果用户名重复，他的数量变成1
        :param username:
        :return: count 数量
        """
        count = Users.objects.filter(username=username).count()

        # json格式
        data = {
            'count': count,
            'username': username
        }
        return res_json(errmsg='你是111个四杀啊啊', data=data)

    # def post(self):
    #     pass


# 手机号验证
# class CheckMobileView(View):
#     def get(self, request, mobile):
#         """
#         routermobiles/(?P<mobile>1[3-9]\d{9})/
#         :param request:
#         :param mobile:
#         :return:
#         """
#         count = Users.objects.filter(mobile=mobile).count()
#
#         # json格式
#         data = {
#             'count': count,
#             'mobile': mobile
#         }
#         # return JsonResponse(data=data)
#
#         # return res_json(errmsg='你是个四杀啊啊', data=data)




class CheckMobileView(View):
    """
    Check whether the user exists
    GET mobiles/(?P<mobile>1[3-9]\d{9})/
    """
    def get(self, request, mobile):
        data = {
            'mobile': mobile,
            'count': Users.objects.filter(mobile=mobile).count()
        }
        return JsonResponse({'data':data})

class SmsCodeView(View):
    def post(self, request):
        """
        手机号 uuid 图形验证码
            'mobile': $mobile.val(),
            'text': text,
            'image_code_id': image_code_uuid,
        :param request:
        :return:
        """
        # 参数接收
        json_str = request.body
        if not json_str:
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')  # 4103
        dict_data = json.loads(json_str)
        image_code_client = dict_data.get('text')
        uuid = dict_data.get('image_code_id')
        mobile = dict_data.get('mobile')

        # 参数验证
        if not all([image_code_client, uuid, mobile]):
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')

        # 连接数据库
        redis_conn = get_redis_connection('verify_code')
        image_code_server = redis_conn.get('img_{}'.format(uuid))
        if image_code_server is None:
            return res_json(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])

        # 删除数据库的验证码，防止重复测试
        try:
            redis_conn.delete('img_{}'.format(uuid))
        except Exception as e:
            logger.error(e)

        # 比对
        image_code_server = image_code_server.decode()
        if image_code_client.lower() != image_code_server.lower():  # lower转小写
            return res_json(errno=Code.PARAMERR, errmsg='验证码输入有误')

        # 生成短信验证码 补全
        sms_code = '%06d' % random.randint(0, 999999)

        # 存到数据库，下一次使用
        redis_conn.setex('sms_{}'.format(mobile), 300, sms_code)
        # 标记手机号在60秒内有发送过短信
        redis_conn.setex('sms_flag_{}'.format(mobile),60,1)
        logger.info('短信验证码是:{}'.format(sms_code))
        # logging.info('发送短信成功[mobile:{} sms_code:{}'.format(mobile, sms_code))

        # 调用接口发短信,发短信要钱
        # ccp = CCP()
        # ccp.send_template_sms(mobile, [sms_code, 5], 1)
        send_sms_code.delay(mobile, sms_code)
        return res_json(errmsg='短信验证码发送成功')


send_sms = SmsCodeView.as_view()
