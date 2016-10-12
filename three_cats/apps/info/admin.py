from modeltranslation.admin import TranslationAdmin

from django.contrib import admin

from apps.info.models import Info, Carousel, Infophoto, Stores


class InfoAdmin(admin.ModelAdmin):
    fieldsets = [
        (u'Info', {'fields': ('topic', 'title', 'image', 'video', 'info')})
    ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]


class StoresAdmin(admin.ModelAdmin):
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


class CarouselAdmin(admin.ModelAdmin):
    list_display = ('image', 'order',)


class InfophotoAdmin(admin.ModelAdmin):
    list_display = ('info', 'image',)


admin.site.register(Info, InfoAdmin)


admin.site.register(Carousel, CarouselAdmin)


admin.site.register(Infophoto, InfophotoAdmin)


admin.site.register(Stores, StoresAdmin)
