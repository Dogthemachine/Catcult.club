import os
from pygeocoder import Geocoder

from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile

from django.db import models
from django.utils.translation import ugettext_lazy as _

from PIL import Image


class Info(models.Model):
    topic = models.CharField(_('topic'), max_length=50, unique=True, db_index=True)
    title = models.CharField(_('name'), max_length=250, blank=True)
    image = models.ImageField(upload_to='info', blank=True)
    video = models.CharField(_('video'), max_length=1000, default='', blank=True)
    info = models.TextField(_('text'), default='', blank=True)
    address = models.CharField(_('address'), max_length=250, blank=True)
    latlon = models.CharField(_('lat lon'), max_length=50, blank=True)

    class Meta:
        verbose_name = _('Info')
        verbose_name_plural = _('Info')

    def __unicode__(self):
        return u'%s' % self.topic

    def save(self, *args, **kwargs):
        if self.address:
            self.latlon = Geocoder.geocode(self.address)[0].coordinates
        super(Info, self).save(*args, **kwargs)


class Maintitle(models.Model):
    image = models.ImageField(upload_to='info')
    order = models.SmallIntegerField(_('order'), default=10)
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('order',)
        verbose_name = _('Photo Title')
        verbose_name_plural = _('Photo Title')

    def __unicode__(self):
        return u'%s' % self.added


class Stores(models.Model):
    name = models.CharField(_('name'), max_length=250)
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    small_image = models.ImageField(upload_to='small_photos/%Y/%m/%d', blank=True, editable=False)
    description = models.TextField(_('description'), blank=True, default='')
    order_is_available = models.PositiveSmallIntegerField(_('order is available'), default=0)
    web_address = models.CharField(_('web_address'), max_length=250, blank=True, null=True, default=None)
    added = models.DateTimeField(_('added'), auto_now_add=True)
    sequence = models.PositiveSmallIntegerField(_('sequence'), default=0)

    class Meta:
        ordering = ('sequence',)
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


class Infophoto(models.Model):
    info = models.ForeignKey(Info)
    image = models.ImageField(upload_to='info')
    small_image = models.ImageField(upload_to='small_info', blank=True, editable=False)
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('-added',)
        verbose_name = _('Info Photo')
        verbose_name_plural = _('Info Photo')

    def __unicode__(self):
        return u'%s' % self.added

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

        super(Infophoto, self).save(*args, **kwargs)
