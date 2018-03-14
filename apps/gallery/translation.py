from modeltranslation.translator import translator, TranslationOptions

from apps.gallery.models import Gallery


class GalleryTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

translator.register(Gallery, GalleryTranslationOptions)
