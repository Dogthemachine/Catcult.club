from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from apps.elephants.models import Items


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
    item = models.ForeignKey(Items)

    class Meta:
        ordering = ('order',)
        verbose_name = _('Order items')
        verbose_name_plural = _('Order items')

    def __unicode__(self):
        return u'%s' % self.order


class Cart(models.Model):
    item = models.ForeignKey(Items)
    session_key = models.CharField(_('name'), max_length=32)
    amount = models.SmallIntegerField(_('amount'))
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('added',)
        verbose_name = _('Cart')
        verbose_name_plural = _('Cart')

    def __unicode__(self):
        return u'%s' % self.session_key