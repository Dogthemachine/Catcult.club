from django.contrib import admin
from apps.elephants.models import Items, Photo, Categories, Fashions, Sizes, Balance
from modeltranslation.admin import TranslationAdmin


class ItemsAdmin(TranslationAdmin):

    list_display = ('name', 'added', 'price', 'price_description', 'description', 'fashions',)

    fieldsets = [
        (u'Items', {'fields': ('name', 'image', 'description', 'details', 'price', 'price_description', 'fashions',)})
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


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'details', 'sequence',)


class FashionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'categories', 'details', 'sequence',)


class SizesAdmin(admin.ModelAdmin):
    list_display = ('name', 'categories', 'description', 'sequence',)


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('item', 'size', 'amount',)


admin.site.register(Items, ItemsAdmin)


admin.site.register(Photo, PhotoAdmin)


admin.site.register(Categories, CategoriesAdmin)


admin.site.register(Fashions, FashionsAdmin)


admin.site.register(Sizes, SizesAdmin)


admin.site.register(Balance, BalanceAdmin)