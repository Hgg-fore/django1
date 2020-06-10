# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect, HttpResponseRedirect
from . import models
from django.http import JsonResponse
from hashlib import sha1


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
            red = HttpResponseRedirect('/user/info/')
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


def user_info(request):
    return render(request, 'df_user/user_center_info.html')