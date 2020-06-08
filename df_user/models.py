from django.db import models


# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=40)
    email = models.CharField(max_length=30)


class UserAddress(models.Model):
    recipient = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    postcode = models.CharField(max_length=6)
    phone = models.CharField(max_length=11)
    user = models.ForeignKey(UserInfo)
