from modeltranslation.admin import TranslationAdmin

from django.contrib import admin

from apps.orders.models import Cart, Orders, OrderItems, Payment, PaymentRaw


class CartAdmin(admin.ModelAdmin):
    list_display = ('session_key',)

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone')

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'balance',)


class PaymentRawAdmin(admin.ModelAdmin):
    list_display = ('added',)


admin.site.register(Cart, CartAdmin)


admin.site.register(Orders, OrdersAdmin)


admin.site.register(OrderItems, OrderItemsAdmin)


admin.site.register(Payment)


admin.site.register(PaymentRaw, PaymentRawAdmin)
