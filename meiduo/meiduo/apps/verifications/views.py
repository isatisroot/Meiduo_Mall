from django.http import HttpResponse
from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework.views import APIView
from . import constants
from meiduo.libs.captcha.captcha import Captcha
# Create your views here.

class ImageView(APIView):
    def get(self, request, image_code_id):
        # 1. 生成验证码
        # text 表示图片中的文本验证码
        # image 表示生成的图片
        captcha = Captcha()
        text, image = captcha.generate_captcha()

        # 2. 保存文本格式验证码到redis中
        # 2.1 获取redis在django中的连接对象，参数就是配置文件中字典成员下标
        redis = get_redis_connection('verify')
        # 2.2 往对象添加键值对
        redis.setex("image_code_id: %s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        # 3. 响应验证码图片
        return HttpResponse(image, content_type="image/jpg")
