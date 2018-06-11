from modeltranslation.admin import TranslationAdmin

from django.contrib import admin

from apps.gallery.models import Gallery


class GalleryAdmin(TranslationAdmin):
    list_display = ('added', 'items', 'name')


admin.site.register(Gallery, GalleryAdmin)
