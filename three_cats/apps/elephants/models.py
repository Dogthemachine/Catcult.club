import os
from cStringIO import StringIO

from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.signals import post_save, post_delete
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models import Sum


class Categories(models.Model):
    name = models.CharField(_('name'), max_length=70)
    icon_a = models.ImageField(upload_to='small_photos/%Y/%m/%d', blank=True, editable=False, default='')
    icon_b = models.ImageField(upload_to='small_photos/%Y/%m/%d', blank=True, editable=False, default='')
    icon_c = models.ImageField(upload_to='small_photos/%Y/%m/%d', blank=True, editable=False, default='')
    details = models.TextField(_('details'), blank=True)
    sequence = models.PositiveSmallIntegerField(_('sequence'), default=0)

    class Meta:
        ordering = ('sequence',)
        verbose_name = _('Categories of items')
        verbose_name_plural = _('Categories of items')

    def __unicode__(self):
        return u'%s' % self.name

    def get_fashions(self):
        return Fashions.objects.filter(categories=self)


class Fashions(models.Model):
    name = models.CharField(_('name'), max_length=70, default='No name')
    categories = models.ForeignKey(Categories)
    icon_a = models.ImageField(upload_to='small_photos/%Y/%m/%d', blank=True, editable=False, default='')
    icon_b = models.ImageField(upload_to='small_photos/%Y/%m/%d', blank=True, editable=False, default='')
    icon_c = models.ImageField(upload_to='small_photos/%Y/%m/%d', blank=True, editable=False, default='')
    details = models.TextField(_('details'), blank=True, default='')
    sequence = models.PositiveSmallIntegerField(_('sequence'), default=0)

    class Meta:
        ordering = ('sequence',)
        verbose_name = _('Fashions of items')
        verbose_name_plural = _('Fashions of items')

    def __unicode__(self):
        return u'%s' % self.name


class Sizes(models.Model):
    name = models.CharField(_('name'), max_length=20)
    categories = models.ForeignKey(Categories)
    description = models.TextField(_('description'), blank=True, default='')
    sequence = models.PositiveSmallIntegerField(_('sequence'), default=0)

    class Meta:
        ordering = ('sequence',)
        verbose_name = _('Sizes of items')
        verbose_name_plural = _('Sizes of items')

    def __unicode__(self):
        return u'%s' % self.name


class Items(models.Model):
    name = models.CharField(_('name'), max_length=250)
    fashions = models.ForeignKey(Fashions)
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    small_image = models.ImageField(upload_to='small_photos/%Y/%m/%d', blank=True, editable=False)
    description = models.TextField(_('description'), blank=True, default='')
    details = models.TextField(_('details'), blank=True, default='')
    price = models.PositiveSmallIntegerField(_('price'), default=0)
    price_description = models.CharField(_('price_description'), max_length=250, default='')
    views_per_month = models.PositiveSmallIntegerField(_('sequence'), default=0)
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

    def get_balance(self):
        return Balance.objects.filter(item=self)

    def get_amount(self):
        return Balance.objects.filter(item=self).aggregate(Sum('amount'))


class Items_views(models.Model):
    item = models.ForeignKey(Items)
    added = models.DateTimeField(_('added'), auto_now_add=True)


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


class Balance(models.Model):
    item = models.ForeignKey(Items)
    size = models.ForeignKey(Sizes)
    amount = models.PositiveSmallIntegerField(_('amount'), default=0)

    class Meta:
        verbose_name = _('Amount of items')
        verbose_name_plural = _('Amount of items')

    def __unicode__(self):
        return u'%s' % self.item


@receiver(post_save, sender=Items)
def create_item_balance(sender, instance, created, **kwargs):
    if created:
        category = instance.fashions.categories
        sizes = Sizes.objects.filter(categories=category)
        for size in sizes:
            balance = Balance(item=instance, size=size)
            balance.save()


@receiver(post_save, sender=Sizes)
def create_size_balance(sender, instance, created, **kwargs):
    if created:
        category = instance.categories
        items = Items.objects.filter(fashions__categories=category)
        for item in items:
            balance = Balance(item=item, size=instance)
            balance.save()