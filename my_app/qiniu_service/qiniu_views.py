from django.conf import settings
from qiniu import Auth, put_file, etag

from django.shortcuts import render, HttpResponse
from app01.models import Picture, Admin
from rest_framework.views import APIView

access_key = settings.QINIU_ACCESS_KEY
secret_key = settings.QINIU_SECRET_KEY


class UploadView(APIView):
    def get(self, request):

        #构建鉴权对象
        q = Auth(access_key, secret_key)

        #要上传的空间
        bucket_name = 'six-jiang'

        #上传到七牛后保存的文件名
        key = 'my-python-logo.png'

        #生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name, key, 3600)

        #要上传文件的本地路径
        localfile = 'app01/photo.jpeg'

        ret, info = put_file(token, key, localfile)
        if info.status_code == 200:
            Picture.objects.create(title='第一张', image=settings.QINIU_DOMAIN + key)
        return HttpResponse('ok')
