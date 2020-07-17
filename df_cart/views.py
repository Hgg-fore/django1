from django.shortcuts import render, redirect
from .models import *
from df_user import user_decorator
from django.http import JsonResponse


# Create your views here.
@user_decorator.login
def cart(request):
    user_id = request.session.get('user_id')
    carts = CartInfo.objects.filter(user_id=int(user_id))
    context = {'carts': carts}
    return render(request, 'df_cart/cart.html', context)


@user_decorator.login
def add(request, gid, count):
    uid = request.session.get('user_id')
    gid = int(gid)
    count = int(count)
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    if len(carts) >= 1:
        cart0 = carts[0]
        cart0.count += count
    else:
        cart0 = CartInfo()
        cart0.user_id = uid
        cart0.goods_id = gid
        cart0.count = count
    cart0.save()

    if request.is_ajax():
        count = CartInfo.objects.filter(user=request.session['user_id']).count()
        return JsonResponse({'count': count})
    else:
        return redirect('/cart/')


@user_decorator.login
def edit(request, cart_id, count):
    try:
        cart0 = CartInfo.objects.get(pk=int(cart_id))
        cart0.count = int(count)
        data = {'ok': 0}
        cart0.save()
    except Exception as e:
        data = {'ok': count}
    return JsonResponse(data)


@user_decorator.login
def delete(request, cart_id):
    try:
        cart0 = CartInfo.objects.get(pk=int(cart_id))
        cart0.delete()
        data = {'ok': 1}
    except Exception as e:
        data = {'ok': 0}
    return JsonResponse(data)
