from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:id>', views.item, name='item'),
    path('cart', views.cart, name='cart'),
    path('cart/add/<int:id>', views.cart_add, name='cart_add'),
    path('cart/remove/<int:id>', views.cart_remove, name='cart_remove'),
    path('buy/<int:id>', views.buy_item, name='buy_item'),
    path('buy/', views.buy_cart, name='buy_cart'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('success/', views.success_payment, name='success_payment'),
    path('apply_promo/', views.apply_promo, name='apply_promo'),
    path('', views.main, name='main')
    ]