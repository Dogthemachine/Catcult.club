import os
from io import BytesIO

from django_resized import ResizedImageField
from PIL import Image

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


class Categories(models.Model):
    name = models.CharField(_('name'), max_length=70)
    image = ResizedImageField(size=[300, 150], upload_to='photos/%Y/%m/%d')
    image_hover = ResizedImageField(size=[300, 150], upload_to='photos/%Y/%m/%d')
    details = models.TextField(_('details'), blank=True)
    sequence = models.PositiveSmallIntegerField(_('sequence'), default=0)

    class Meta:
        ordering = ('sequence',)
        verbose_name = _('Categories of items')
        verbose_name_plural = _('Categories of items')

    def __str__(self):
        return u'%s' % self.name

    def get_fashions(self):
        return Fashions.objects.filter(categories=self)


class Fashions(models.Model):
    name = models.CharField(_('name'), max_length=70, default='No name')
    categories = models.ForeignKey(Categories)
    image = ResizedImageField(size=[300, 150], upload_to='photos/%Y/%m/%d')
    image_hover = ResizedImageField(size=[300, 150], upload_to='photos/%Y/%m/%d')
    details = models.TextField(_('details'), blank=True, default='')
    sequence = models.PositiveSmallIntegerField(_('sequence'), default=0)

    class Meta:
        ordering = ('sequence',)
        verbose_name = _('Fashions of items')
        verbose_name_plural = _('Fashions of items')

    def __str__(self):
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

    def __str__(self):
        return u'%s' % self.name


class Items(models.Model):
    name = models.CharField(_('name'), max_length=250)
    fashions = models.ForeignKey(Fashions)
    image = ResizedImageField(size=[1500, 1500], upload_to='photos/%Y/%m/%d')
    image_small = ResizedImageField(size=[300, 300], crop=['middle', 'center'], upload_to='small_photos/%Y/%m/%d')
    description = models.TextField(_('description'), blank=True, default='')
    details = models.TextField(_('details'), blank=True, default='')
    price = models.PositiveSmallIntegerField(_('price'), default=0)
    price_description = models.CharField(_('price_description'), max_length=250, default=_('Grn.'))
    views_per_month = models.PositiveSmallIntegerField(_('sequence'), default=0)
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('added',)
        verbose_name = _('items')
        verbose_name_plural = _('items')

    def __str__(self):
        return u'%s' % self.name

    def get_balance(self):
        return Balance.objects.filter(item=self)

    def get_amount(self):
        balances = Balance.objects.filter(item=self)
        for balance in balances:
            if balance.amount > 0:
                return True
        return False

    def sorting(self):
        return Balance.objects.filter(item=self).aggregate(Sum('amount')) * self.views_per_month


class Items_views(models.Model):
    item = models.ForeignKey(Items)
    added = models.DateTimeField(_('added'), auto_now_add=True)


class Photo(models.Model):
    item = models.ForeignKey(Items)
    image = ResizedImageField(size=[1500, 1500], upload_to='photos/%Y/%m/%d')
    image_small = ResizedImageField(size=[300, 300], crop=['middle', 'center'], upload_to='small_photos/%Y/%m/%d')
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('added',)
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')

    def __str__(self):
        return u'%s - %s' % (self.item.name, self.added)


class Balance(models.Model):
    item = models.ForeignKey(Items)
    size = models.ForeignKey(Sizes)
    amount = models.IntegerField(_('amount'), default=0)

    class Meta:
        verbose_name = _('Amount of items')
        verbose_name_plural = _('Amount of items')

    def __str__(self):
        return u'%s - %s - %s' % (self.item.name, self.size.name, self.amount)


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
