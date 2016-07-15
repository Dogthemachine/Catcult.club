# -*- coding: utf-8 -*-

from modeltranslation.translator import translator, TranslationOptions
from apps.elephants.models import Items, Stores, Categories, Fashions


class ItemsTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели Items.
    """

    fields = ('name', 'description', 'details', 'price_description',)


class StoresTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели Stores.
    """

    fields = ('name', 'description',)


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

translator.register(Stores, StoresTranslationOptions)

translator.register(Fashions, FashionsTranslationOptions)

translator.register(Categories, CategoriesTranslationOptions)