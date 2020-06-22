# -*- coding:utf-8 -*-
from django.db import models
from tinymce.models import HTMLField


# Create your models here.
class TypeInfo(models.Model):
    title = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.title.encode('utf-8')


class GoodsInfo(models.Model):
    title = models.CharField(max_length=20)
    pic = models.ImageField(upload_to='df_goods')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    isDelete = models.BooleanField(default=False)
    unit = models.CharField(max_length=20)
    # 简介
    intro = models.CharField(max_length=200)
    # 商品详情
    details = HTMLField()
    # 人气
    popularity = models.IntegerField()
    # 库存
    inventory = models.IntegerField()
    type = models.ForeignKey(TypeInfo)
