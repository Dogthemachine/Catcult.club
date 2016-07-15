import os
from cStringIO import StringIO

from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class Categories(models.Model):
    name = models.CharField(_('name'), max_length=70, default='No name')
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    small_image = models.ImageField(upload_to='small_photos/%Y/%m/%d', blank=True, editable=False)
    details = models.TextField(_('details'), blank=True, default='')
    sequence = models.PositiveSmallIntegerField(_('price'), default=0)

    class Meta:
        ordering = ('sequence',)
        verbose_name = _('Categories of items')
        verbose_name_plural = _('Categories of items')

    def __unicode__(self):
        return u'%s' % self.name

    def save(self, *args, **kwargs):
        SIZE = (300, 300)

        image = Image.open(self.image)

        small_image = image.copy()

        small_image.thumbnail(SIZE, Image.ANTIALIAS)

        temp_handle = StringIO()
        small_image.save(temp_handle, 'JPEG')
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1][:-4] + '.jpg',
                                 temp_handle.read(),
                                 content_type='image/jpeg')
        self.small_image.save(suf.name, suf, save=False)

        super(Categories, self).save(*args, **kwargs)


class Fashions(models.Model):
    name = models.CharField(_('name'), max_length=70, default='No name')
    categories = models.ForeignKey(Categories)
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    small_image = models.ImageField(upload_to='small_photos/%Y/%m/%d', blank=True, editable=False)
    details = models.TextField(_('details'), blank=True, default='')
    sequence = models.PositiveSmallIntegerField(_('price'), default=0)

    class Meta:
        ordering = ('sequence',)
        verbose_name = _('Fashions of items')
        verbose_name_plural = _('Fashions of items')

    def __unicode__(self):
        return u'%s' % self.name

    def save(self, *args, **kwargs):
        SIZE = (300, 300)

        image = Image.open(self.image)

        small_image = image.copy()

        small_image.thumbnail(SIZE, Image.ANTIALIAS)

        temp_handle = StringIO()
        small_image.save(temp_handle, 'JPEG')
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1][:-4] + '.jpg',
                                 temp_handle.read(),
                                 content_type='image/jpeg')
        self.small_image.save(suf.name, suf, save=False)

        super(Fashions, self).save(*args, **kwargs)


class Stores(models.Model):
    name = models.CharField(_('name'), max_length=250)
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    small_image = models.ImageField(upload_to='small_photos/%Y/%m/%d', blank=True, editable=False)
    description = models.TextField(_('description'), blank=True, default='')
    order_is_available = models.PositiveSmallIntegerField(_('order is available'), default=0)
    web_address = models.CharField(_('web_address'), max_length=250, blank=True, null=True, default=None)
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('added',)
        verbose_name = _('stores')
        verbose_name_plural = _('stores')

    def __unicode__(self):
        return u'%s' % self.name

    def save(self, *args, **kwargs):
        SIZE = (300, 300)

        image = Image.open(self.image)

        small_image = image.copy()

        small_image.thumbnail(SIZE, Image.ANTIALIAS)

        temp_handle = StringIO()
        small_image.save(temp_handle, 'JPEG')
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1][:-4] + '.jpg',
                                 temp_handle.read(),
                                 content_type='image/jpeg')
        self.small_image.save(suf.name, suf, save=False)

        super(Stores, self).save(*args, **kwargs)


class Items(models.Model):
    name = models.CharField(_('name'), max_length=250)
    fashions = models.ForeignKey(Fashions)
    stores = models.ManyToManyField(Stores, blank=True, null=True, default=None)
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    small_image = models.ImageField(upload_to='small_photos/%Y/%m/%d', blank=True, editable=False)
    description = models.TextField(_('description'), blank=True, default='')
    details = models.TextField(_('details'), blank=True, default='')
    price = models.PositiveSmallIntegerField(_('price'), default=0)
    price_description = models.CharField(_('price_description'), max_length=250, default='')
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('added',)
        verbose_name = _('items')
        verbose_name_plural = _('items')

    def __unicode__(self):
        return u'%s' % self.name

    def save(self, *args, **kwargs):
        SIZE = (300, 300)

        image = Image.open(self.image)

        small_image = image.copy()

        small_image.thumbnail(SIZE, Image.ANTIALIAS)

        temp_handle = StringIO()
        small_image.save(temp_handle, 'JPEG')
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1][:-4] + '.jpg',
                                 temp_handle.read(),
                                 content_type='image/jpeg')
        self.small_image.save(suf.name, suf, save=False)

        super(Items, self).save(*args, **kwargs)

class Photo(models.Model):
    item = models.ForeignKey(Items)
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('added',)
        verbose_name = _('Photo')
        verbose_name_plural = _('Photo')

    def __unicode__(self):
        return u'%s' % self.added