from modeltranslation.translator import translator, TranslationOptions

from apps.elephants.models import Items, Categories, Fashions, Sizes


class ItemsTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'details', 'price_description',)


class FashionsTranslationOptions(TranslationOptions):
    fields = ('name', 'details',)


class CategoriesTranslationOptions(TranslationOptions):
    fields = ('name', 'details',)


class SizesTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


translator.register(Items, ItemsTranslationOptions)


translator.register(Fashions, FashionsTranslationOptions)


translator.register(Categories, CategoriesTranslationOptions)


translator.register(Sizes, SizesTranslationOptions)
