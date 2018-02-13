from modeltranslation.translator import translator, TranslationOptions

from apps.info.models import Info, Stores, Config


class InfoTranslationOptions(TranslationOptions):
    fields = ('title', 'info', 'title_tag', 'description_tag',)


class StoresTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

class ConfigTranslationOptions(TranslationOptions):
    fields = ('price_description', 'price_description_usd', 'price_description_eur',)


translator.register(Info, InfoTranslationOptions)

translator.register(Stores, StoresTranslationOptions)

translator.register(Config, ConfigTranslationOptions)
