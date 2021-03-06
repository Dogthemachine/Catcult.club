from modeltranslation.admin import TranslationAdmin

from django.contrib import admin

from apps.orders.models import Cart, Orders, OrderItems, Payment, PaymentRaw, Phones, Promo, Countris, DeliveryCost, IWant


class CartAdmin(admin.ModelAdmin):
    list_display = ('session_key',)


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone')


class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'balance',)


class PaymentRawAdmin(admin.ModelAdmin):
    list_display = ('added',)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'comment')


class PhonesAdmin(admin.ModelAdmin):
    list_display = ('phone', 'news')


class PromoAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'used')


class CountrisAdmin(admin.ModelAdmin):
    list_display = ('name',)


class IWantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'status', 'added',)


class DeliveryCostAdmin(admin.ModelAdmin):
    list_display = ('country', 'weigth_from', 'weigth_to', 'cost',)


admin.site.register(Cart, CartAdmin)


admin.site.register(Orders, OrdersAdmin)


admin.site.register(OrderItems, OrderItemsAdmin)


admin.site.register(Payment, PaymentAdmin)


admin.site.register(Promo, PromoAdmin)


admin.site.register(PaymentRaw, PaymentRawAdmin)


admin.site.register(Phones, PhonesAdmin)


admin.site.register(Countris, CountrisAdmin)


admin.site.register(IWant, IWantAdmin)


admin.site.register(DeliveryCost, DeliveryCostAdmin)
