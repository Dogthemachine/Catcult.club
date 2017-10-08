from modeltranslation.admin import TranslationAdmin

from django.contrib import admin

from apps.elephants.models import Items, Photo, Categories, Fashions, Sizes, Balance, Stocks, Sets, SetsPhoto


class PhotoInline(admin.TabularInline):
    model = Photo


class SetsPhotoInline(admin.TabularInline):
    model = SetsPhoto


class ItemsAdmin(TranslationAdmin):
    inlines = [PhotoInline]

    list_display = ('name', 'added', 'price', 'price_description', 'description', 'fashions',)

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


class SetsAdmin(TranslationAdmin):
    inlines = [SetsPhotoInline]

    list_display = ('name', 'added', 'price', 'price_description', 'description', 'categories',)

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


class CategoriesAdmin(TranslationAdmin):
    list_display = ('name', 'details', 'sequence',)


class FashionsAdmin(TranslationAdmin):
    list_display = ('name', 'categories', 'details', 'displayed', 'sequence', 'weigth',)


class SizesAdmin(admin.ModelAdmin):
    list_display = ('name', 'categories', 'description', 'sequence',)


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('item', 'size', 'amount',)


class StocksAdmin(TranslationAdmin):
    list_display = ('action_begin', 'action_end', 'name', 'discount',)


admin.site.register(Items, ItemsAdmin)


admin.site.register(Sets, SetsAdmin)


admin.site.register(Categories, CategoriesAdmin)


admin.site.register(Fashions, FashionsAdmin)


admin.site.register(Sizes, SizesAdmin)


admin.site.register(Balance, BalanceAdmin)


admin.site.register(Stocks, StocksAdmin)
