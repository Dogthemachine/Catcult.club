from django.contrib import admin
from apps.moderation.models import Corrections, Advent
from modeltranslation.admin import TranslationAdmin


class CorrectionsAdmin(admin.ModelAdmin):
    list_display = ('balance', 'user', 'amount', 'added',)

class AdventAdmin(admin.ModelAdmin):
    list_display = ('balance', 'user', 'amount',)

admin.site.register(Corrections, CorrectionsAdmin)

admin.site.register(Advent, AdventAdmin)
