from django_resized import ResizedImageField
from solo.models import SingletonModel

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _


class Info(models.Model):
    topic = models.CharField(_('topic'), max_length=50, unique=True, db_index=True)
    title = models.CharField(_('name'), max_length=250, blank=True)
    image = ResizedImageField(size=[1500, 1500], upload_to='info', blank=True)
    video = models.CharField(_('video'), max_length=1000, default='', blank=True)
    info = models.TextField(_('text'), default='', blank=True)
    title_tag = models.CharField(_('title tag'), max_length=70, blank=True, default='')
    description_tag = models.CharField(_('description tag'), max_length=280, blank=True, default='')

    class Meta:
        verbose_name = _('Info')
        verbose_name_plural = _('Infos')

    def __str__(self):
        return u'%s' % self.topic


class Carousel(models.Model):
    image = ResizedImageField(size=[1500, 1500], upload_to='info')
    order = models.SmallIntegerField(_('order'), default=0)
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('order',)
        verbose_name = _('Photo Title')
        verbose_name_plural = _('Photo Titles')

    def __str__(self):
        return u'%s' % self.added


class Stores(models.Model):
    name = models.CharField(_('name'), max_length=250)
    image = ResizedImageField(size=[1500, 1500], upload_to='info')
    small_image = ResizedImageField(size=[300, 300], crop=['middle', 'center'], upload_to='small_info', blank=True)
    description = models.TextField(_('description'), blank=True, default='')
    order_is_available = models.PositiveSmallIntegerField(_('order is available'), default=0)
    web_address = models.CharField(_('web_address'), max_length=250, blank=True)
    added = models.DateTimeField(_('added'), auto_now_add=True)
    sequence = models.PositiveSmallIntegerField(_('sequence'), default=0)

    class Meta:
        ordering = ('sequence',)
        verbose_name = _('Stores')
        verbose_name_plural = _('Stores')

    def __str__(self):
        return u'%s' % self.name


class Infophoto(models.Model):
    info = models.ForeignKey(Info)
    image = ResizedImageField(size=[1500, 1500], upload_to='info')
    small_image = ResizedImageField(size=[300, 300], crop=['middle', 'center'], upload_to='small_info', blank=True)
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('-added',)
        verbose_name = _('Info Photo')
        verbose_name_plural = _('Info Photos')

    def __str__(self):
        return u'%s - %s' % (self.info, self.added)


class Config(SingletonModel):
    dollar_rate = models.DecimalField(_('dollar rate'), max_digits=5, decimal_places=2, default=1)
    euro_rate = models.DecimalField(_('euro rate'), max_digits=5, decimal_places=2, default=1)
    price_description = models.CharField(_('price_description'), max_length=250, default=ugettext('Grn.'))
    price_description_usd = models.CharField(_('price_description'), max_length=250, default=ugettext('Usd.'))
    price_description_eur = models.CharField(_('price_description'), max_length=250, default=ugettext('Eur.'))
    static = models.CharField(_('static url'), max_length=250, default='https://catcult.club/static/')
    media = models.CharField(_('media url'), max_length=250, default='https://catcult.club/media/')

    class Meta:
        ordering = ('dollar_rate',)
        verbose_name = _('Config')
        verbose_name_plural = _('Config')

    def __str__(self):
        return u'%s' % self.dollar_rate