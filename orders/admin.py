from django.contrib import admin

from orders.models import Order, OrderItem, Discount


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('total_amount', 'user', 'discount', 'order_number',
                    'is_paid', 'is_active', 'get_total_amount')
    readonly_fields = ['get_total_amount']
    fields = ['total_amount', 'user', 'discount', 'order_number',
              'is_paid', 'is_active', 'get_total_amount']
    ...


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    ...


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    ...
