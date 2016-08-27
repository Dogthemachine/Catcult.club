# -*- coding: utf-8 -*-

from modeltranslation.translator import translator, TranslationOptions
from apps.elephants.models import Items, Categories, Fashions


class ItemsTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели Orders.
    """

    fields = ('name', 'description', 'details', 'price_description',)


class FashionsTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели Fashions.
    """

    fields = ('name', 'details',)


class CategoriesTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели Categories.
    """

    fields = ('name', 'details',)


translator.register(Items, ItemsTranslationOptions)

translator.register(Fashions, FashionsTranslationOptions)

translator.register(Categories, CategoriesTranslationOptions)