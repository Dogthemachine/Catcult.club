# -*- coding: utf-8 -*-

from modeltranslation.translator import translator, TranslationOptions
from apps.info.models import Info


class InfoTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели Info.
    """

    fields = ('title', 'info',)


translator.register(Info, InfoTranslationOptions)