from modeltranslation.admin import TranslationAdmin

from django.contrib import admin

from apps.orders.models import Cart, Orders, OrderItems


class CartAdmin(admin.ModelAdmin):
    list_display = ('session_key',)

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'balance',)


admin.site.register(Cart, CartAdmin)


admin.site.register(Orders, OrdersAdmin)


admin.site.register(OrderItems, OrderItemsAdmin)
