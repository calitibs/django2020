import json
import re
from django.contrib.auth import login, logout
from django_redis import get_redis_connection
from django.shortcuts import render, redirect, reverse
from django.views import View
from django2020.utils.response_code import res_json, Code, error_map
from django2020.utils.captcha.captcha import captcha
# Create your views here.

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django_redis import get_redis_connection
import logging

from users.models import Users

logger = logging.getLogger('django')


def demo(request):
    return HttpResponse('hello world')


def index(request):
    """
    1 准备css js image
    2 准备html
    :param request:
    :return:
    """
    # return render(request, '/index.html')
    # return render(request, 'base/base.html')
    # return render(request, 'users/register.html')
    return render(request, 'news/index.html')


s = index


def register(request):
    return render(request, 'users/register.html')
    # return render(request, 'news/index.html')


# 图形验证
def Image_code(request, img_id):
    text, image = captcha.generate_captcha()
    redis_conn = get_redis_connection('verify_code')  # 连接数据库
    # 保存id键 60存在时间 text值
    redis_conn.setex('img_{}'.format(img_id).encode('utf8'), 60, text)
    logger.info('图形验证码是：{}'.format(text))

    # 设置过期时间
    # request.session['image_code'] = text
    # request.session.set_expiry(60)
    # print(request.session.keys())
    # print(111, request.session.get('image_code'))

    return HttpResponse(content=image, content_type='image/jpg')


class RegisterView(View):

    def get(self, request):
        print('get')
        return render(request, 'users/register.html')

    def post(self, request):
        print('post')
        # js=request.POST.get('username')
        # js1=json.loads(js)
        js_str = request.body
        if not js_str:
            res_json(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        dict_data = json.loads(js_str)

        username = dict_data.get('username')
        password = dict_data.get('password')
        password2 = dict_data.get('password_repeat')
        mobile = dict_data.get('mobile')
        sms_code = dict_data.get('sms_code')
        # 判断所有参数是否为空
        if not all([username, password, password2, mobile, sms_code]):
            return HttpResponseForbidden('请填写准确的参数')

        # 验证每一个参数
        # 用户名
        if not re.match('^[\u4e00-\u9fa5\w]{5,20}$', username):
            return HttpResponseForbidden('用户名输入错误，必须为6~12位中英')
        if Users.objects.filter(username=username).count() > 0:
            return HttpResponseForbidden('用户名已存在，请重新输入')

        # 密码
        if not re.match('^[0-9A-Za-z]{6,20}$', password):
            return HttpResponseForbidden('密码输入格式错误，必须为6~20位中英数字')
        if password != password2:
            # return HttpResponseForbidden('两次密码输入不一致')
            return res_json(errno=Code.PARAMERR, errmsg='两次密码输入不一致，请重新输入')
        #
        # 手机号
        if not re.match('^1[345789]\d{9}$', mobile):
            return HttpResponseForbidden('手机号格式错误，必须为11位数字，首位为1，次位为3~91-')
        if Users.objects.filter(mobile=mobile).count() > 0:
            return HttpResponseForbidden('手机号已存在，请重新输入')

        # 验证码校验
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_' + mobile)  # 是一个byte类型，需要解码
        print('*************', sms_code_server)
        # 判断验证码是否过期
        if sms_code_server is None:
            return res_json(errno=Code.PARAMERR, errmsg='参数错误，验证码已过期')

        # 用完就删
        redis_conn.delete('sms_{}'.format(mobile))
        redis_conn.delete('sms_flag_{}'.format(mobile))

        # 判断是否正确
        if sms_code != sms_code_server.decode():
            return HttpResponseForbidden('短信验证码错误')
        print(sms_code, sms_code_server)
        # 创建用户
        user = Users.objects.create_user(username=username, password=password, mobile=mobile)

        # 保存连接（创建完用户直接可以登录）
        login(request, user)

        # 返回
        return res_json(errno=Code.PARAMERR, errmsg='恭喜你，成功注册为本网站会员')
        # return res_json(errno=Code.OK, errmsg='恭喜你，成功注册为本网站会员')


from .forms import LoginForm


# 登录
class LoginView(View):
    def get(self, request):
        title = '登录页面飞走了'
        return render(request, 'users/login.html', context={'title': title})

    # is_authenticated =true/false # 如果验证成功返回true
    def post(self, request):
        js_str = request.body
        if not js_str:
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')

        dict_data = json.loads(js_str.decode())

        # 数据验证 使用form表单验证
        form = LoginForm(data=dict_data, request=request)
        if form.is_valid():
            # 表单验证成功处理
            return res_json(errno=Code.OK)
        else:
            # 表单验证失败处理
            msg_list = []
            for i in form.errors.get_json_data().values():
                msg_list.append(i[0].get('message'))
            msg_str = '/'.join(msg_list)
            return res_json(errno=Code.PARAMERR, errmsg=msg_str)


# 退出
class LogOut(View):
    def get(self, request):
        logout(request)
        return redirect('/')


# 修改密码
class CheckPwd(View):

    def get(self, request):
        return render(request, 'users/check_pawd.html')

    def post(self, request):
        mobile = request.POST.get('telephone')
        old = request.POST.get('old_password')
        new = request.POST.get('new_password')

        if not all([mobile, old, new]):
            return HttpResponseForbidden('参数不能为空')

        # mobile = re.match(r'^1[3-9]\d{9}$',mobile)
        # if not mobile:
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseForbidden('手机号有误，请重新输入')


        user = Users.objects.get(mobile=mobile)
        if user:
            try:
                user.check_password(old)
            except Exception as e:
                return HttpResponseForbidden('原始密码输入错误')
            # 密码验证
            if not re.match(r'^[0-9A-Za-z]{6,20}$', new):
                return HttpResponseForbidden('密码格式错误')
            # 密码对比
            if old == new:
                return HttpResponseForbidden('新旧密码不能相同')
            # 密码修改保存
            user.set_password(new)  # 加密
            user.save()
            res = redirect(reverse('users:login'))
            return res
        else:
            return HttpResponseForbidden('用户账号不存在')


# 密码找回
class Passwd(View):
    def get(self,request):
        return render(request,'users/c_pwd.html')

    def post(self, request):
        pass
        # 处理短信验证码
        # 密码验证
        # 拿到当前对象
        # 密码保存到数据库



P=Passwd.as_view()
LogOut = LogOut.as_view()
check = CheckPwd.as_view()
lo = LoginView.as_view()
# 方法二
reg = RegisterView.as_view()
