from django.contrib import admin
from apps.info.models import Info, Maintitle, Infophoto
from modeltranslation.admin import TranslationAdmin

class InfoAdmin(TranslationAdmin):
    fieldsets = [
        (u'Info', {'fields': ('topic', 'title', 'image', 'video', 'info', 'address',)})
    ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

class MaintitleAdmin(admin.ModelAdmin):
    list_display = ('image', 'order',)

class InfophotoAdmin(admin.ModelAdmin):
    list_display = ('info', 'image',)

admin.site.register(Info, InfoAdmin)

admin.site.register(Maintitle, MaintitleAdmin)

admin.site.register(Infophoto, InfophotoAdmin)
