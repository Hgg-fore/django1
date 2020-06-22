from django.shortcuts import render
from .models import TypeInfo, GoodsInfo
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    types = TypeInfo.objects.all()
    goods_0_1 = types[0].goodsinfo_set.order_by('id')[0:4]
    goods_0_2 = types[0].goodsinfo_set.order_by('-popularity')[0:4]
    context = {'goods_0_1':goods_0_1, 'goods_0_2': goods_0_2,}
    return render(request, 'df_goods/index.html', context)


def list_view(request, type_id, p_index, sort_rule):
    typeinfo = TypeInfo.objects.get(pk=int(type_id))
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if sort_rule == '1':
        goods = GoodsInfo.objects.filter(type=int(type_id)).order_by('-id')
    elif sort_rule == '2':
        goods = GoodsInfo.objects.filter(type=int(type_id)).order_by('-price')
    elif sort_rule == '3':
        goods = GoodsInfo.objects.filter(type=int(type_id)).order_by('-popularity')
    paginator = Paginator(goods, 10)
    page = paginator.page(int(p_index))
    context = {'paginator': paginator, 'page': page,
               'typeinfo': typeinfo, 'sort': sort_rule,
               'news': news,
               }
    return render(request, 'df_goods/list.html', context)


def detail(request, good_id):
    goods = GoodsInfo.objects.get(pk=int(good_id))
    goods.popularity += 1
    goods.save()
    news = goods.type.goodsinfo_set.order_by('-id')[0:2]
    context = {'goods': goods, 'news': news,
               }
    return render(request, 'df_goods/detail.html', context)