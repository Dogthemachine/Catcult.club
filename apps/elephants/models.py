from django_resized import ResizedImageField

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Categories(models.Model):
    name = models.CharField(_('name'), max_length=70)
    image = ResizedImageField(size=[300, 150], upload_to='photos/%Y/%m/%d', blank=True)
    image_hover = ResizedImageField(size=[300, 150], upload_to='photos/%Y/%m/%d', blank=True)
    image_en = ResizedImageField(size=[300, 150], upload_to='photos/%Y/%m/%d', blank=True)
    image_hover_en = ResizedImageField(size=[300, 150], upload_to='photos/%Y/%m/%d', blank=True)
    details = models.TextField(_('details'), blank=True)
    set = models.BooleanField(_('set'), default=False)
    title_tag = models.CharField(_('title tag'), max_length=70, blank=True, default='')
    description_tag = models.CharField(_('description tag'), max_length=280, blank=True, default='')
    sequence = models.PositiveSmallIntegerField(_('sequence'), default=0)
    showcase_displayed = models.BooleanField(_('showcase_displayed'), default=True)

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
    image_en = ResizedImageField(size=[300, 150], upload_to='photos/%Y/%m/%d', blank=True)
    image_hover_en = ResizedImageField(size=[300, 150], upload_to='photos/%Y/%m/%d', blank=True)
    cost_price = models.PositiveSmallIntegerField(_('cost price'), default=0)
    weigth = models.PositiveSmallIntegerField(_('weigth'), default=0)
    details = models.TextField(_('details'), blank=True, default='')
    displayed = models.BooleanField(_('displayed'), default=True)
    title_tag = models.CharField(_('title tag'), max_length=70, blank=True, default='')
    description_tag = models.CharField(_('description tag'), max_length=280, blank=True, default='')
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


class Artists(models.Model):
    name = models.CharField(_('name'), max_length=250)
    image = ResizedImageField(size=[300, 150], upload_to='photos/%Y/%m/%d', blank=True)
    description = models.TextField(_('description'), blank=True, default='')
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Artists')
        verbose_name_plural = _('Artists')

    def __str__(self):
        return self.name


class Items(models.Model):
    name = models.CharField(_('name'), max_length=250)
    fashions = models.ForeignKey(Fashions)
    artist = models.ForeignKey(Artists, blank=True, null=True)
    image = ResizedImageField(size=[2500, 2500], upload_to='photos/%Y/%m/%d')
    image_small = ResizedImageField(size=[300, 300], crop=['middle', 'center'], upload_to='small_photos/%Y/%m/%d', editable=False)
    description = models.TextField(_('description'), blank=True, default='')
    details = models.TextField(_('details'), blank=True, default='')
    price = models.PositiveSmallIntegerField(_('price'), default=0)
    price_description = models.CharField(_('price_description'), max_length=250, default=_('Grn.'))
    views = models.PositiveIntegerField(_('views'), default=0)
    views_today = models.PositiveIntegerField(_('views today'), default=0)
    views_month = models.CharField(_('views month'), default=0, max_length=512)
    showcase_displayed = models.BooleanField(_('showcase_displayed'), default=True)
    title_tag = models.CharField(_('title tag'), max_length=70, blank=True, default='')
    description_tag = models.CharField(_('description tag'), max_length=280, blank=True, default='')
    rozetka = models.BooleanField(_('to rozetka'), default=False)
    description_rozetka_a = models.TextField(_('description rozetka a'), blank=True, default='')
    description_rozetka_b = models.TextField(_('description rozetka b'), blank=True, default='')
    description_rozetka_c = models.TextField(_('descriptionrozetka c'), blank=True, default='')
    description_rozetka_d = models.TextField(_('descriptionrozetka d'), blank=True, default='')
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('-views',)
        verbose_name = _('items')
        verbose_name_plural = _('items')

    def __str__(self):
        return u'%s (%s) (%s)' % (self.name, self.fashions.name, self.description)

    def save(self, *args, **kwargs):
        if not self.image._committed:
            self.image_small = self.image.file
        super().save(*args, **kwargs)

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

    def get_actual_price(self):
        price = self.price

        global_stock = Stocks.objects.filter(categories__isnull=True, fashions__isnull=True,
                                             action_begin__lte=timezone.datetime.today(),
                                             action_end__gte=timezone.datetime.today()).order_by('-id')[:1]

        if not global_stock:
            stock = Stocks.objects.filter(categories=self.fashions.categories,
                                          action_begin__lte=timezone.datetime.today(),
                                          action_end__gte=timezone.datetime.today()).order_by('-id')[:1]
            if not stock:
                stock = Stocks.objects.filter(fashions=self.fashions,
                                              action_begin__lte=timezone.datetime.today(),
                                              action_end__gte=timezone.datetime.today()).order_by('-id')[:1]
        else:
            stock = global_stock

        if stock and stock[0].type == 0:
            price = price - price * stock[0].discount // 100

        return price

    def get_discount(self):
        discount = 0

        global_stock = Stocks.objects.filter(categories__isnull=True, fashions__isnull=True,
                                             action_begin__lte=timezone.datetime.today(),
                                             action_end__gte=timezone.datetime.today()).order_by('-id')[:1]

        if not global_stock:
            stock = Stocks.objects.filter(categories=self.fashions.categories,
                                          action_begin__lte=timezone.datetime.today(),
                                          action_end__gte=timezone.datetime.today()).order_by('-id')[:1]
            if not stock:
                stock = Stocks.objects.filter(fashions=self.fashions,
                                              action_begin__lte=timezone.datetime.today(),
                                              action_end__gte=timezone.datetime.today()).order_by('-id')[:1]
        else:
            stock = global_stock

        if stock and stock[0].type == 0:
            discount = self.price * stock[0].discount // 100

        return discount

    def get_discount_name(self):

        global_stock = Stocks.objects.filter(categories__isnull=True, fashions__isnull=True,
                                             action_begin__lte=timezone.datetime.today(),
                                             action_end__gte=timezone.datetime.today()).order_by('-id')[:1]

        if not global_stock:
            stock = Stocks.objects.filter(categories=self.fashions.categories,
                                          action_begin__lte=timezone.datetime.today(),
                                          action_end__gte=timezone.datetime.today()).order_by('-id')[:1]
            if not stock:
                stock = Stocks.objects.filter(fashions=self.fashions,
                                              action_begin__lte=timezone.datetime.today(),
                                              action_end__gte=timezone.datetime.today()).order_by('-id')[:1]
        else:
            stock = global_stock

        return stock[0].name


class Sets(models.Model):
    name = models.CharField(_('name'), max_length=250)
    categories = models.ForeignKey(Categories)
    items = models.ManyToManyField(Items)
    image = ResizedImageField(size=[2500, 2500], upload_to='photos/%Y/%m/%d')
    image_small = ResizedImageField(size=[300, 300], crop=['middle', 'center'], upload_to='small_photos/%Y/%m/%d', editable=False)
    description = models.TextField(_('description'), blank=True, default='')
    details = models.TextField(_('details'), blank=True, default='')
    price = models.PositiveSmallIntegerField(_('price'), default=0)
    price_description = models.CharField(_('price_description'), max_length=250, default=_('Grn.'))
    views = models.PositiveIntegerField(_('views'), default=0)
    views_today = models.PositiveIntegerField(_('views today'), default=0)
    views_month = models.CharField(_('views month'), default=0, max_length=512)
    title_tag = models.CharField(_('title tag'), max_length=70, blank=True, default='')
    description_tag = models.CharField(_('description tag'), max_length=280, blank=True, default='')
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('-views',)
        verbose_name = _('Sets')
        verbose_name_plural = _('Sets')

    def __str__(self):
        return u'%s' % self.name

    def save(self, *args, **kwargs):
        if not self.image._committed:
            self.image_small = self.image.file
        super().save(*args, **kwargs)

    def get_balance(self):
        return Balance.objects.filter(item__sets=self)

    def get_amount(self):
        items = Items.objects.filter(sets=self)
        res = False
        if items:
            res = True
        for item in items:
            balances = Balance.objects.filter(item=item)
            am = False
            for balance in balances:
                if balance.amount > 0:
                    am = True
            res = res and am
        return res

    def sorting(self):
        items = Items.objects.filter(sets=self)
        res = 0
        if items:
            res = 1
        for item in items:
            balances = Balance.objects.filter(item=item)
            am = 0
            for balance in balances:
                if balance.amount > 0:
                    am = 1
            res = res * am
        return res * self.views_per_month

    def get_actual_price(self):
        price = self.price

        global_stock = Stocks.objects.filter(categories__isnull=True, action_begin__lte=timezone.datetime.today(), action_end__gte=timezone.datetime.today()).order_by('-id')[:1]

        if not global_stock:
            stock = Stocks.objects.filter(categories=self.categories, action_begin__lte=timezone.datetime.today(), action_end__gte=timezone.datetime.today()).order_by('-id')[:1]
        else:
            stock = global_stock

        if stock and stock[0].type == 0:
            price = price - price * stock[0].discount // 100

        return price

    def get_discount(self):
        discount = 0

        global_stock = Stocks.objects.filter(categories__isnull=True, action_begin__lte=timezone.datetime.today(), action_end__gte=timezone.datetime.today()).order_by('-id')[:1]

        if not global_stock:
            stock = Stocks.objects.filter(categories=self.categories, action_begin__lte=timezone.datetime.today(), action_end__gte=timezone.datetime.today()).order_by('-id')[:1]
        else:
            stock = global_stock

        if stock and stock[0].type == 0:
            discount = self.price * stock[0].discount // 100

        return discount

    def get_discount_name(self):
        global_stock = Stocks.objects.filter(categories__isnull=True, action_begin__lte=timezone.datetime.today(), action_end__gte=timezone.datetime.today()).order_by('-id')[:1]

        if not global_stock:
            stock = Stocks.objects.filter(categories=self.categories, action_begin__lte=timezone.datetime.today(), action_end__gte=timezone.datetime.today()).order_by('-id')[:1]
        else:
            stock = global_stock

        return stock[0].name


class Photo(models.Model):
    item = models.ForeignKey(Items)
    image = ResizedImageField(size=[2500, 2500], upload_to='photos/%Y/%m/%d')
    image_small = ResizedImageField(size=[300, 300], crop=['middle', 'center'], upload_to='small_photos/%Y/%m/%d', editable=False)
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('added',)
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')

    def save(self, *args, **kwargs):
        if not self.image._committed:
            self.image_small = self.image.file
        super().save(*args, **kwargs)

    def __str__(self):
        return u'%s - %s' % (self.item.name, self.added)


class RPhoto(models.Model):
    item = models.ForeignKey(Items)
    image = ResizedImageField(size=[2500, 2500], upload_to='photos/%Y/%m/%d')
    image_small = ResizedImageField(size=[300, 300], crop=['middle', 'center'], upload_to='small_photos/%Y/%m/%d', editable=False)
    weight = models.PositiveSmallIntegerField(_('position'), default=0)
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('added',)
        verbose_name = _('RozetkaPhoto')
        verbose_name_plural = _('RozetkaPhotos')

    def save(self, *args, **kwargs):
        if not self.image._committed:
            self.image_small = self.image.file
        super().save(*args, **kwargs)

    def __str__(self):
        return u'%s - %s' % (self.item.name, self.added)


class SetsPhoto(models.Model):
    set = models.ForeignKey(Sets)
    image = ResizedImageField(size=[2500, 2500], upload_to='photos/%Y/%m/%d')
    image_small = ResizedImageField(size=[300, 300], crop=['middle', 'center'], upload_to='small_photos/%Y/%m/%d', editable=False)
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        ordering = ('added',)
        verbose_name = _('Sets photo')
        verbose_name_plural = _('Sets photos')

    def save(self, *args, **kwargs):
        if not self.image._committed:
            self.image_small = self.image.file
        super().save(*args, **kwargs)

    def __str__(self):
        return u'%s - %s' % (self.set.name, self.added)


class Balance(models.Model):
    item = models.ForeignKey(Items)
    size = models.ForeignKey(Sizes)
    amount = models.IntegerField(_('amount'), default=0)

    class Meta:
        ordering = ('id',)
        verbose_name = _('Amount of items')
        verbose_name_plural = _('Amount of items')

    def __str__(self):
        return u'%s - %s - %s' % (self.item.name, self.size.name, self.amount)


class Stocks(models.Model):
    name = models.CharField(_('name'), max_length=250)
    categories = models.ManyToManyField(Categories, blank=True)
    fashions = models.ManyToManyField(Fashions, blank=True)
    type = models.PositiveSmallIntegerField(_('type'), choices=settings.STOCKS_TYPES)
    items_count = models.PositiveSmallIntegerField(_('items count'), blank=True, default=0)
    image = ResizedImageField(size=[2500, 2500], upload_to='photos/%Y/%m/%d', blank=True)
    description = models.TextField(_('description'), blank=True, default='')
    discount = models.PositiveSmallIntegerField(_('discount'), default=0)
    action_begin = models.DateField(_('action_begin'))
    action_end = models.DateField(_('action_end'))

    class Meta:
        ordering = ('action_begin',)
        verbose_name = _('stocks')
        verbose_name_plural = _('stocks')

    def __str__(self):
        return u'%s' % self.name


class BalanceLog(models.Model):
    balance = models.ForeignKey(Balance)
    old_value = models.IntegerField(_('old value'))
    new_value = models.IntegerField(_('new value'))
    arrival = models.BooleanField(_('arrival'), default=False)
    user = models.ForeignKey(User)
    change_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-change_time',)
        verbose_name = _('Balance log')
        verbose_name_plural = _('Balance logs')

    def __str__(self):
        return "%s - %s" % (self.balance, self.change_time)


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
