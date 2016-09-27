from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from apps.elephants.models import Balance, Items, Sizes


class Orders(models.Model):
    name = models.CharField(_('name'), max_length=70)
    phone = models.CharField(_('phone'), max_length=32)
    email = models.EmailField(_('email'), default='')
    city = models.CharField(_('city'), max_length=32, default='')
    delivery = models.CharField(_('delivery'), max_length=32, default=0)
    payment = models.CharField(_('payment'), max_length=32, default=0)
    message = models.TextField(_('message'), default='')
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
    balance = models.ForeignKey(Balance)

    class Meta:
        ordering = ('order',)
        verbose_name = _('Order items')
        verbose_name_plural = _('Order items')

    def __unicode__(self):
        return u'%s' % self.order


class Cart(models.Model):
    session_key = models.CharField(_('name'), max_length=32)
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('added',)
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return u'%s' % self.session_key

    def get_total(self):
        items = CartItem.objects.filter(cart=self)
        total = 0
        for item in items:
            total += item.item.price * item.amount
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart)
    item = models.ForeignKey(Items)
    size = models.ForeignKey(Sizes)
    amount = models.PositiveSmallIntegerField()
