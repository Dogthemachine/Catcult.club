from modeltranslation.translator import translator, TranslationOptions

from apps.orders.models import Countris, NovaPoshtaCities, NovaPoshtaWarehouses, NovaPoshtaRegions


class CountrisTranslationOptions(TranslationOptions):
    fields = ('name',)


class NovaPoshtaCitiesTranslationOptions(TranslationOptions):
    fields = ('description',)


class NovaPoshtaWarehousesTranslationOptions(TranslationOptions):
    fields = ('description',)

class NovaPoshtaRegionsTranslationOptions(TranslationOptions):
    fields = ('description',)


translator.register(Countris, CountrisTranslationOptions)

translator.register(NovaPoshtaRegions, NovaPoshtaRegionsTranslationOptions)

translator.register(NovaPoshtaCities, NovaPoshtaCitiesTranslationOptions)

translator.register(NovaPoshtaWarehouses, NovaPoshtaWarehousesTranslationOptions)
