from modeltranslation.translator import translator, TranslationOptions

from apps.orders.models import Countris


class CountrisTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Countris, CountrisTranslationOptions)
