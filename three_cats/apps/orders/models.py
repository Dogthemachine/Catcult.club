from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from apps.elephants.models import Balance, Items, Sizes


class Orders(models.Model):
    name = models.CharField(_('name'), max_length=70)
    phone = models.CharField(_('phone'), max_length=32)
    comment = models.TextField(_('comment'), default='', blank=True)
    delivery = models.IntegerField(_('delivery'), choices=settings.DELIVERY, default=0)
    payment = models.IntegerField(_('payment'), choices=settings.PAYMENT, default=0)
    status = models.IntegerField(_('status'), choices=settings.ORDER_STATUS, default=0)
    ttn = models.IntegerField(_('TTN'), default=0)
    sms_sent = models.BooleanField(_('SMS sent'), default=False)
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('-added',)
        verbose_name = _('Orders')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return u'%s' % self.name

    def get_total_price(self):
        items = OrderItems.objects.filter(order=self)
        sum = 0

        for i in items:
            sum += i.balance.item.price * i.amount

        return sum


class OrderItems(models.Model):
    order = models.ForeignKey(Orders)
    balance = models.ForeignKey(Balance)
    amount = models.PositiveIntegerField(_('amount'))
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('added',)
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')

    def __str__(self):
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

    def check_avail(self):
        balance = Balance.objects.get(item=self.item, size=self.size)

        if balance.amount == 0:
            return False
        else:
            return True


@receiver(post_save, sender=OrderItems)
def update_balance_on_order(sender, instance, created, **kwargs):
    if created:
        balance = instance.balance
        balance.amount = balance.amount - instance.amount
        balance.save()


@receiver(post_delete, sender=OrderItems)
def update_balance_or_order_delete(sender, instance, **kwargs):
    balance = instance.balance
    balance.amount = balance.amount + instance.amount
    balance.save()
