# -*- coding:utf-8 -*-
from hashlib import sha1

from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from df_goods.models import GoodsInfo
from . import models
from . import user_decorator


# Create your views here.
def register(request):
    context = {'title': '注册'}
    return render(request, 'df_user/register.html', context)


def register_handle(request):
    post = request.POST
    name = post.get('user_name')
    pwd = post.get('pwd')
    cpwd = post.get('cpwd')
    email = post.get('email')
    # 再一次判断两次输入密码是否相等
    if pwd != cpwd:
        return redirect('/user/register/')
    user = models.UserInfo.users.create_user(name, pwd, email)
    user.save()
    return redirect('/user/login/')


def register_exist(request):
    name = request.GET.get('user_name')
    num = models.UserInfo.users.filter(name=name).count()
    return JsonResponse({'data': num})


def login(request):
    username = request.COOKIES.get('username', '')
    context = {'username': username, 'error_name': 0, 'error_pwd': 0, 'title': '登录'}
    return render(request, 'df_user/login.html', context)


def logout(request):
    request.session.flush()
    return redirect('/')


def login_handle(request):
    post = request.POST
    name = post.get('username')
    pwd = post.get('pwd')
    rem = post.get('remember', 0)
    # 根据用户名查询对象
    users = models.UserInfo.users.filter(name=name)
    if len(users) == 1:
        s1 = sha1()
        s1.update(pwd)
        if s1.hexdigest() == users[0].pwd:
            url = request.COOKIES.get('url', '/')
            # print(url)
            red = HttpResponseRedirect(url)
            if rem != 0:
                red.set_cookie('username', name)
            else:
                red.delete_cookie('username')
            request.session['user_id'] = users[0].id
            request.session['user_name'] = name
            return red
        else:
            context = {'username': name, 'error_name': 0, 'error_pwd': 1, 'title': '登录'}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'error_name': 1, 'error_pwd': 0, 'title': '登录'}
        return render(request, 'df_user/login.html', context)


@user_decorator.login
def user_info(request):
    user_id = request.session.get('user_id')
    user_name = request.session.get('user_name')
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_list = []
    if goods_ids != '':
        goods_ids_list = goods_ids.split(',')
        for goods_id in goods_ids_list:
            goods_list.append(GoodsInfo.objects.get(id=goods_id))
    context = {'username': user_name, 'user_id': user_id, 'last_view_goods': goods_list}
    print goods_list
    return render(request, 'df_user/user_center_info.html', context)
