from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.


class Admin(models.Model):
    nickname = models.CharField(max_length=255, null=True)
    account = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    phone = models.CharField('手机号码', max_length=30)
    deleted = models.BooleanField(default=False)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)


class Picture(models.Model):
    title = models.CharField(max_length=255, null=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    image = models.URLField()
    deleted = models.BooleanField(default=False)


