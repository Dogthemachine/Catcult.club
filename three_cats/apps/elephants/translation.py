from modeltranslation.translator import translator, TranslationOptions

from apps.elephants.models import Items, Categories, Fashions


class ItemsTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'details', 'price_description',)


class FashionsTranslationOptions(TranslationOptions):
    fields = ('name', 'details',)


class CategoriesTranslationOptions(TranslationOptions):
    fields = ('name', 'details',)


translator.register(Items, ItemsTranslationOptions)


translator.register(Fashions, FashionsTranslationOptions)


translator.register(Categories, CategoriesTranslationOptions)
