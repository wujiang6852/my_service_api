from django.conf.urls import url, include
from qiniu_service import qiniu_views

urlpatterns = [
    url('^upload', qiniu_views.UploadView.as_view(), name='上传图片')

]