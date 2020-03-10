from django.shortcuts import render, redirect

# Create your views here.
from django2020.QQLoginTool.QQtool import OAuthQQ

from django.views import View
from django.http import HttpResponse
# from django.conf import settings
from django2020.settings import dev


# QQ_STATE=''
class QQAuthView(View):
    print(11)
    def get(self, request):
        # QQ_STATE = request.META['HTTP_REFERER']
        state = request.META['HTTP_REFERER']
        auth = OAuthQQ(
            client_id=dev.app_id, client_secret=dev.ak, redirect_uri=dev.red_url, state=state
        )
        login_url = auth.get_qq_url()
        print(login_url)
        return redirect(login_url)


def demo(requset):
    print(1111111111)
    return HttpResponse('hello world')

auth_callback = demo
