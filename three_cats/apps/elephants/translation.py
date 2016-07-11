# -*- coding: utf-8 -*-

from modeltranslation.translator import translator, TranslationOptions
from apps.elephants.models import Item, Stores


class ItemTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели Item.
    """

    fields = ('name', 'description', 'details', 'price_description', 'price_description_rub',)


class StoresTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели Item.
    """

    fields = ('name', 'description',)


translator.register(Item, ItemTranslationOptions)

translator.register(Stores, StoresTranslationOptions)