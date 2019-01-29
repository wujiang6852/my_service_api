from django.conf.urls import url, include
from app01 import views

urlpatterns = [
    url('^admin$', views.UserViews.as_view(), name='用户'),

]