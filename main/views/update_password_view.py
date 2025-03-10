import random
import traceback

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

from django.core.cache import cache
from django.core.mail import EmailMessage
from django.template import loader

from main.throttles import AnonEmailRateThrottle, UserEmailRateThrottle
from poetry_system import settings

import re

def isEmailValid(email):
    return re.fullmatch(
        re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'),
        email
    )

# 密码必须为8~16位，数字+英文字母+特殊符号
def isPasswordValid(password):
    return re.fullmatch(
        re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#.$@!%&*?])[A-Za-z\d#.$@!%&*?]{8,16}'),
        password
    )


    # email=909140058@qq.com&code=726340&password=wei20475cy.&password2=wei20475cy.
class UpdatePasswordView(APIView):
    
    def get_throttles(self):
        throttle_classes = []
        if self.request.method == 'GET':
            throttle_classes = [AnonEmailRateThrottle, UserEmailRateThrottle]
        # return throttle_classes
        return [throttle() for throttle in throttle_classes]

    def get(self, request):
        arg = request.GET
        try:
            email = arg.get("email", "").strip()

            # # 判断邮箱格式
            # if not isEmailValid(email):
            #     return Response({'result': '邮箱格式有误！'}, status=status.HTTP_400_BAD_REQUEST)

            # 判断邮箱是否是已经注册的状态存在
            exists = User.objects.filter(email=email).exists()
            if not exists:
                return Response({'result': '该邮箱未注册！'}, status=status.HTTP_400_BAD_REQUEST)

            email_title = "修改密码验证码"

            # 这里是生成随机验证码
            code = str(random.randrange(100000, 999999))
            cache.set(email + '_update_password', code, 60 * 5)  # 存session

            # 这个context这里定义的字段，是要给html模板中的验证码使用的，HTML中{% code %}引用即可
            context = {'code': code}

            email_template_name = 'update_password_email.html'
            t = loader.get_template(email_template_name)
            html_content = t.render(context)
            msg = EmailMessage(email_title,  # 邮件主题
                               html_content,  # 邮件内容，使用html模板
                               settings.EMAIL_FROM,  # 用于发送邮件的用户
                               [email]  # 接收邮件的用户列表
                               )

            # 指定邮箱发送的类型
            msg.content_subtype = 'html'

            # 发送邮箱
            send_status = msg.send()

            if not send_status:
                return Response({'result': f'发送邮箱失败,{send_status["errmsg"]}'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'result': "邮件发送成功~\n验证码5分钟有效。",}, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response({'result': "邮件发送失败！"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        arg = request.POST
        try:
            code = arg.get("code")
            email = arg.get("email", "").strip()
            password = arg.get("password", "").strip()
            password2 = arg.get("password2", "").strip()
            key = email + '_update_password'
            store_code = cache.get(key)


            # # 判断邮箱格式
            # if not isEmailValid(email):
            #     return Response({'result': '邮箱格式有误！'}, status=status.HTTP_400_BAD_REQUEST)

            # 判断邮箱是否是已经注册的状态存在
            exists = User.objects.filter(email=email).exists()
            if not exists:
                return Response({'result': '该邮箱未注册！'}, status=status.HTTP_400_BAD_REQUEST)

            # 判断验证码
            if store_code != code:
                # print(store_code, code)
                return Response({'result': "验证码错误或过期！",}, status=status.HTTP_400_BAD_REQUEST)

            # 判断密码格式
            if not isPasswordValid(password):
                return Response({'result': "密码不符合规范！",}, status=status.HTTP_400_BAD_REQUEST)

            # 判断两次输入密码是否一样
            if password != password2:
                return Response({'result': "两次输入密码不一致！",}, status=status.HTTP_400_BAD_REQUEST)


            user = User.objects.get(email=email)
            cache.delete(key) # 删除缓存

            user.set_password(password)
            user.save()

            return Response({'result': "修改密码成功，请重新登录~",}, status=status.HTTP_201_CREATED)

        except Exception as e:
            traceback.print_exc()
            return Response({'result': "修改密码失败"} ,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

