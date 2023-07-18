from django.urls import path, re_path

from orders.views import CartView, CartActionView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    re_path(r'cart/(?P<action>add|remove|clear|pay)/',
            CartActionView.as_view(),
            name='cart_action'),
]
