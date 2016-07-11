from django.contrib import admin
from apps.elephants.models import (Item, Photo, Cart, Orders, Orderitems, Stores)
from modeltranslation.admin import TranslationAdmin


class ItemAdmin(TranslationAdmin):

    list_display = ('name', 'added', 'price', 'price_description', 'description',)

    filter_horizontal = ('stores',)

    fieldsets = [
        (u'Item', {'fields': ('name', 'image', 'stores', 'description', 'details', 'price', 'price_description', 'price_description_rub',)})
    ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
            '/static/modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/modeltranslation/js/tabbed_translation_fields.js',
        ]

        css = {
            'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css',),
        }


class StoresAdmin(TranslationAdmin):
    fieldsets = [
        (u'Stores', {'fields': ('name', 'image', 'description', 'web_address', 'order_is_available',)})
    ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
            '/static/modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/modeltranslation/js/tabbed_translation_fields.js',
        ]

        css = {
            'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css',),
        }


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('item', 'image',)


class CartAdmin(admin.ModelAdmin):
    list_display = ('item', 'amount', 'session_key',)


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'city', 'delivery', 'payment', 'massage', 'cost', 'status',)

class OrderitemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'item',)

admin.site.register(Item, ItemAdmin)

admin.site.register(Stores, StoresAdmin)

admin.site.register(Photo, PhotoAdmin)

admin.site.register(Cart, CartAdmin)

admin.site.register(Orders, OrdersAdmin)

admin.site.register(Orderitems, OrderitemsAdmin)