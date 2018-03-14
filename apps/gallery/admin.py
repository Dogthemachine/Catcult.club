from modeltranslation.admin import TranslationAdmin

from django.contrib import admin

from apps.gallery.models import Gallery


class GalleryAdmin(TranslationAdmin):
    fieldsets = [
        (u'Gallery', {'fields': ('name', 'image', 'description')})
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


admin.site.register(Gallery, GalleryAdmin)
