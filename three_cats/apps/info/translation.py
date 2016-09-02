# -*- coding: utf-8 -*-

from modeltranslation.translator import translator, TranslationOptions
from apps.info.models import Info, Stores


class InfoTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели Info.
    """

    fields = ('title', 'info',)


class StoresTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели Info.
    """

    fields = ('name', 'description',)


translator.register(Info, InfoTranslationOptions)

translator.register(Stores, StoresTranslationOptions)