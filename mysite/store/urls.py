
from django.contrib import admin
from django.urls import path,re_path, include
from . import views

urlpatterns = [
    re_path('^$|^login/$', views.login, name='login'),
    path('logout/', views.logout,name = 'logout_view'),
    path('register/', views.register, name = 'register'),
    path('main/', views.main, name = 'main'),
    path('list/', views.GoodsListView.as_view(), name = 'list'),
    path('detail/', views.show_goods_detail, name = 'detail'),
    path('add/', views.add_cart),
    path('show_cart/', views.show_cart, name = 'cart_view'),
    path('submit_orders/', views.submit_orders),


]
