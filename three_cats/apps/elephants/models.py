import os
from cStringIO import StringIO

from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


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


class Item(models.Model):
    name = models.CharField(_('name'), max_length=250)
    fashions = models.ManyToManyField(Fashions, blank=True, null=True, default=None)
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
        verbose_name = _('item')
        verbose_name_plural = _('item')

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

        super(Item, self).save(*args, **kwargs)

class Photo(models.Model):
    item = models.ForeignKey(Item)
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('added',)
        verbose_name = _('Photo')
        verbose_name_plural = _('Photo')

    def __unicode__(self):
        return u'%s' % self.added


class Cart(models.Model):
    item = models.ForeignKey(Item)
    session_key = models.CharField(_('name'), max_length=32)
    amount = models.SmallIntegerField(_('amount'))
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('added',)
        verbose_name = _('Cart')
        verbose_name_plural = _('Cart')

    def __unicode__(self):
        return u'%s' % self.session_key


class Orders(models.Model):
    name = models.CharField(_('name'), max_length=70, default='No name')
    phone = models.CharField(_('phone'), max_length=32, default='')
    email = models.EmailField(_('email'))
    city = models.CharField(_('city'), max_length=32, default='')
    delivery = models.CharField(_('delivery'), max_length=32, default=0)
    payment = models.CharField(_('payment'), max_length=32, default=0)
    massage = models.TextField(_('massage'), default='')
    cost = models.IntegerField(_('cost'), default=0)
    status = models.IntegerField(_('status'), choices=settings.ORDER_STATUS, default=0)
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('-added',)
        verbose_name = _('orders')
        verbose_name_plural = _('orders')

    def __unicode__(self):
        return u'%s' % self.name


class Orderitems(models.Model):
    order = models.ForeignKey(Orders)
    item = models.ForeignKey(Item)

    class Meta:
        ordering = ('order',)
        verbose_name = _('Order items')
        verbose_name_plural = _('Order items')

    def __unicode__(self):
        return u'%s' % self.order

class Fashions(models.Model):
    name = models.CharField(_('name'), max_length=70, default='No name')
    details = models.TextField(_('details'), blank=True, default='')

    class Meta:
        ordering = ('themes',)
        verbose_name = _('Themes of items')
        verbose_name_plural = _('Themes of items')

    def __unicode__(self):
        return u'%s' % self.order