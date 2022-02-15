from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
import random
import datetime
from .forms import LoginForm, RegistrationForm
from .models import Customer, Goods, OrderLineItem, Orders


# Create your views here.
# 登录
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            userid = form.cleaned_data['userid']
            password = form.cleaned_data['password']
            c = Customer.objects.get(id=userid)
            if c is not None and c.password == password:
                # 客户id放到HTTP session中

                request.session['customer_id'] = c.id
                return HttpResponseRedirect('/main/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


# 注册
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            new_customer = Customer()
            new_customer.id = form.cleaned_data['userid']
            new_customer.name = form.cleaned_data['name']
            new_customer.password = form.cleaned_data['password1']
            new_customer.birthday = form.cleaned_data['birthday']
            new_customer.phone = form.cleaned_data['phone']

            new_customer.save()

            return render(request, 'customer_reg_success.html')
    else:
        form = RegistrationForm()

    return render(request, 'customer_reg.html', {'form': form})


def main(request):
    # session 是否有customer id 判断是否已登录
    if not request.session.has_key('customer_id'):
        print("没有登录")
        return HttpResponseRedirect('/login/')
    return render(request, 'main.html')


class GoodsListView(ListView):
    model = Goods
    ordering = ['id']
    # queryset =
    template_name = 'goods_list.html'


def show_goods_detail(request):
    goodsid = request.GET['id']
    goods = Goods.objects.get(id=goodsid)
    return render(request, 'goods_detail.html', {'goods': goods})


# 添加购物车
def add_cart(request):
    # 判断是否已登录
    if not request.session.has_key('customer_id'):
        print("没有登录")
        return HttpResponseRedirect('/login/')

    goodsid = int(request.GET['id'])
    goodsname = request.GET['name']
    goodsprice = float(request.GET['price'])

    #判断session 中是否已经存在购物数据
    if not request.session.has_key('cart'):
        # 如果不存在，则创建一个空的购物车，购物车是一种list
        request.session['cart'] = []

    cart = request.session['cart']

    flag = 0
    for item in cart:
        if item[0] == goodsid: # cart 中有这个数据
            item[3] += 1
            flag = 1
            break
    if flag == 0: # cart 中没有想买的商品
        item = [goodsid, goodsname, goodsprice, 1]
        cart.append(item)

    request.session['cart'] = cart

    print(cart)
    page = request.GET['page']

    if page == 'detail' :
        return HttpResponseRedirect('/detail/?id=' + str(goodsid))
    else:
        return HttpResponseRedirect('/list/')

def show_cart(request):
    if not request.session.has_key('customer_id'):
        print("no login")
        return HttpResponseRedirect('/login/')

    if not request.session.has_key('cart'):
        print("Cart is empty")
        return render(request, 'cart.html', {'list': [], 'total': 0.0  })

    cart = request.session['cart']
    list = []
    total = 0.0
    for item in cart:
        subtotal = item[2] * item[3]
        total += subtotal
        new_item = (item[0], item[1], item[2], item[3], subtotal)
        list.append(new_item)

    return render(request, 'cart.html', {'list': list, 'total': total  })

def submit_orders(request):
    if request.method == 'POST':
        orders = Orders()


        n = random.randint(0, 9)
        d = datetime.datetime.today()
        ordersid = str(int(d.timestamp() * 1e6)) + str(n)
        orders.id = ordersid
        orders.order_date = d
        orders.status = 1
        orders.total = 0.0
        orders.save()

        cart = request.session['cart']
        total = 0.0
        for  item in cart :
            goodsid = item[0]
            goods = Goods.objects.get(id = goodsid)
            quantity = request.POST['quantity_' + str(goodsid)]

            try :
                quantity = int(quantity)
            except:
                quantity = 0

            subtotal = item[2] * quantity
            total += subtotal

            order_line_item = OrderLineItem()
            order_line_item.quantity = quantity
            order_line_item.goods = goods
            order_line_item.orders = orders
            order_line_item.sub_total = subtotal
            order_line_item.save()
        orders.total = total
        orders.save()
        del request.session['cart']
        return render(request,'order_finish.html', {'ordersid': ordersid})

def logout(request):
    if request.session.has_key('customer_id'):
        del request.session['customer_id']
        if request.session.has_key('cart'):
            del request.session['cart']

    return HttpResponseRedirect('/login/')








