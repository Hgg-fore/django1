from django.contrib import admin
from .models import TypeInfo, GoodsInfo


class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


# Register your models here.
admin.site.register(TypeInfo, TypeInfoAdmin)
admin.site.register(GoodsInfo)
