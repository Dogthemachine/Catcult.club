from django.contrib import admin
from apps.orders.models import Cart, Orders, Orderitems
from modeltranslation.admin import TranslationAdmin


class CartAdmin(admin.ModelAdmin):
    list_display = ('session_key',)

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'city', 'delivery', 'payment', 'message', 'cost', 'status',)

class OrderitemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'balance',)

admin.site.register(Cart, CartAdmin)

admin.site.register(Orders, OrdersAdmin)

admin.site.register(Orderitems, OrderitemsAdmin)
