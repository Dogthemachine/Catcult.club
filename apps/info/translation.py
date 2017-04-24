from modeltranslation.translator import translator, TranslationOptions

from apps.info.models import Info, Stores


class InfoTranslationOptions(TranslationOptions):
    fields = ('title', 'info',)


class StoresTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


translator.register(Info, InfoTranslationOptions)

translator.register(Stores, StoresTranslationOptions)
