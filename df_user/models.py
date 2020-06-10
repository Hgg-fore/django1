# -*- coding:utf-8 -*-
from django.db import models
import hashlib


# Create your models here.
class UserInfoManager(models.Manager):
    # 密码加密
    @classmethod
    def encryption_algorithm(cls, pwd):
        a = hashlib.sha1()
        a.update(pwd)
        return a.hexdigest()

    def create_user(self, name, pwd, email):
        user = self.model()
        user.name = name
        user.pwd = UserInfoManager.encryption_algorithm(pwd)
        user.email = email
        return user


class UserInfo(models.Model):
    name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=40)
    email = models.CharField(max_length=30)
    users = UserInfoManager()


class UserAddress(models.Model):
    recipient = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    postcode = models.CharField(max_length=6, null=True)
    phone = models.CharField(max_length=11)
    user = models.ForeignKey(UserInfo)
