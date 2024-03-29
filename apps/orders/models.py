from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from apps.elephants.models import Balance, Items, Sizes, Stocks, Sets
from apps.info.models import Config


class Orders(models.Model):
    name = models.CharField(_("first name"), max_length=70)
    last_name = models.CharField(_("last name"), max_length=70)
    phone = models.CharField(_("phone"), max_length=32, db_index=True)
    comment = models.TextField(_("comment"), default="", blank=True)
    email = models.EmailField(_("email"), max_length=254, null=True, blank=True)
    lang_code = models.CharField(_("lang code"), default="ru", blank=True, max_length=2)
    delivered = models.BooleanField(_("delivered"), default=False)
    paid = models.BooleanField(_("paid"), default=False)
    date_of_delivery = models.DateField(_("date_of_delivery"), blank=True, null=True)
    delivery_method = models.IntegerField(
        _("delivery_method"), choices=settings.DELIVERY, default=0
    )
    delivery_cost = models.IntegerField(_("delivery_cost"), default=0)
    payment_method = models.IntegerField(
        _("payment_method"), choices=settings.PAYMENT, default=0
    )
    liqpay_wait_accept = models.BooleanField(_("LiqPay wait accept"), default=False)
    wfp_status = models.CharField(
        _("WFP status"), max_length=512, default="", blank=True
    )
    user_comment = models.CharField(_("user comment"), max_length=512, blank=True)
    ttn = models.IntegerField(_("TTN"), default=0)
    discount_promo = models.PositiveIntegerField(
        _("discount from promo (percent)"), default=0
    )
    discount_stocks = models.PositiveIntegerField(_("discount from stocks"), default=0)
    discount_set = models.PositiveIntegerField(_("discount from set"), default=0)
    sms_sent = models.BooleanField(_("SMS sent"), default=False)
    packed = models.BooleanField(_("Packed"), default=False)
    added = models.DateTimeField(_("added"), auto_now_add=True)

    class Meta:
        ordering = ("-added",)
        verbose_name = _("Orders")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return u"%s" % self.name

    def get_total_price_grn(self):
        items = OrderItems.objects.filter(order=self)
        sum = 0

        for i in items:
            sum += i.price * i.amount

        sum -= self.discount_stocks
        # sum -= self.discount_set
        if not self.discount_stocks:
            sum = sum - sum * self.discount_promo // 100

        sum += self.delivery_cost

        return sum

    def get_total_price(self, request):
        sum = self.get_total_price_grn()
        if request.session["valuta"] == "grn":
            pass
        else:
            config = Config.objects.get()
            rate = 1
            if request.session["valuta"] == "usd":
                rate = config.dollar_rate
            if request.session["valuta"] == "eur":
                rate = config.euro_rate
            sum = round(sum / rate, 2)

        return sum

    def get_total_paid(self):
        items = Payment.objects.filter(order=self)
        sum = 0

        for i in items:
            sum += i.amount

        return sum

    def get_remaining_amount(self):
        return self.get_total_price_grn() - self.get_total_paid()

    def get_number(self):
        return self.id


class OrderItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    balance = models.ForeignKey(Balance, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(_("amount"))
    price = models.PositiveIntegerField(_("price"), default=0)
    added = models.DateTimeField(_("added"), auto_now_add=True)

    class Meta:
        ordering = ("added",)
        verbose_name = _("Order item")
        verbose_name_plural = _("Order items")

    def __str__(self):
        return u"%s" % self.order


class Phones(models.Model):
    phone = models.CharField(_("phone"), max_length=32, unique=True, db_index=True)
    lang_code = models.CharField(_("lang code"), default="ru", blank=True, max_length=2)
    news = models.BooleanField(_("news"), default=False)
    active = models.BooleanField(_("active"), default=False)

    class Meta:
        ordering = ("phone",)
        verbose_name = _("Phone")
        verbose_name_plural = _("Phone")

    def __str__(self):
        return self.phone


class Payment(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(_("amount"))
    comment = models.CharField(_("comment"), max_length=512)
    token = models.CharField(_("liqpay token"), max_length=512, blank=True)
    sender_phone = models.CharField(_("liqpay sender phone"), max_length=64, blank=True)
    added = models.DateTimeField(_("added"), auto_now_add=True)


class PaymentRaw(models.Model):
    data = models.TextField(_("data"))
    sign = models.TextField(_("sign"))
    data_decoded = models.TextField(_("data decoded"), default="", blank=True)
    added = models.DateTimeField(_("added"), auto_now_add=True)


class Cart(models.Model):
    session_key = models.CharField(_("name"), max_length=32)
    added = models.DateTimeField(_("added"), auto_now_add=True)
    discount_stocks = models.PositiveIntegerField(_("discount from stocks"), default=0)
    comment = models.CharField(_("comment"), max_length=512, blank=True)

    class Meta:
        ordering = ("added",)
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    def __str__(self):
        return u"%s" % self.session_key

    def get_total(self):
        items = CartItem.objects.filter(cart=self)
        total = 0
        for item in items:
            total += item.item.get_actual_price() * (item.amount - item.amount_set)
        for set in self.cartset_set.all():
            total += set.set.get_actual_price() * set.amount
        total -= self.discount_stocks
        return total

    def get_discount(self):
        items = CartItem.objects.filter(cart=self)
        discount = 0
        for item in items:
            discount += item.item.get_discount() * (item.amount - item.amount_set)
        for set in self.cartset_set.all():
            discount += set.set.get_discount() * set.amount
        return discount

    def get_items_count(self):
        stock = Stocks.objects.filter(
            type=1,
            action_begin__lte=timezone.datetime.today(),
            action_end__gte=timezone.datetime.today(),
        ).order_by("-id")[:1]

        message = ""

        if stock:
            count = 0

            cart_items = CartItem.objects.filter(cart=self).order_by("-item__price")

            for i in cart_items:
                count += i.amount

            items = count // (stock[0].items_count + 1)

            sum = 0

            discounted_items = []

            for i in cart_items:
                for j in range(0, i.amount):
                    discounted_items.append(i.item.price)

            n = 0
            for i in discounted_items:
                n += 1
                if n % (stock[0].items_count + 1) == 0:
                    sum += i

            self.discount_stocks = sum
            self.comment = gettext("Your discount is %s UAH.") % sum
            self.save()

            if sum:
                message = gettext(
                    "You have %(items)s discounted items for %(sum)s UAH."
                ) % {"items": items, "sum": sum}

            modulo = count % (stock[0].items_count + 1)
            if modulo == stock[0].items_count:
                message += gettext("You can add one more item and get a discount.")
                # message += stock.description

        return message

    def get_weith(self):
        items = CartItem.objects.filter(cart=self)
        weith = 0
        for item in items:
            weith += item.item.fashions.weigth * (item.amount - item.amount_set)

        return weith

    def discount_stocks_val(self, request):
        discount_stocks = self.discount_stocks
        if request.session["valuta"] == "grn":
            pass
        else:
            config = Config.objects.get()
            rate = 1
            if request.session["valuta"] == "usd":
                rate = config.dollar_rate
            if request.session["valuta"] == "eur":
                rate = config.euro_rate
            discount_stocks = round(discount_stocks / rate, 2)
        return discount_stocks


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    size = models.ForeignKey(Sizes, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()
    amount_set = models.PositiveIntegerField(default=0)

    def check_avail(self):
        balance = Balance.objects.get(item=self.item, size=self.size)

        if balance.amount >= self.amount:
            return True
        else:
            return False


class CartSet(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    set = models.ForeignKey(Sets, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def check_avail(self):
        items = self.set.items
        for item in items:
            balance = Balance.objects.get(item=self.item, size=self.size)

            if balance.amount < self.amount:
                return False

        return True


class CartSetItem(models.Model):
    cartset = models.ForeignKey(CartSet, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    size = models.ForeignKey(Sizes, on_delete=models.CASCADE)


class Promo(models.Model):
    code = models.CharField(_("Code"), max_length=250)
    discount = models.PositiveSmallIntegerField(_("Discount"), default=0)
    used = models.BooleanField(_("Used"), default=False)

    class Meta:
        ordering = ("code",)
        verbose_name = _("code")
        verbose_name_plural = _("code")

    def __str__(self):
        return u"%s" % self.code


class Countris(models.Model):
    name = models.CharField(_("name"), max_length=70)

    class Meta:
        ordering = ("name",)
        verbose_name = _("Countris")
        verbose_name_plural = _("Countris")

    def __str__(self):
        return u"%s" % self.name


class DeliveryCost(models.Model):
    country = models.ForeignKey(Countris, on_delete=models.CASCADE)
    weigth_from = models.PositiveSmallIntegerField()
    weigth_to = models.PositiveSmallIntegerField()
    cost = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ("country",)
        verbose_name = _("Delivery_Cost")
        verbose_name_plural = _("Delivery_Cost")


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


class IWant(models.Model):
    NEW = 100
    VIEWED = 200
    CONTACTED = 230
    NOT_INTEREST = 260
    MADE = 300
    SENT = 400

    STATUS = (
        (NEW, _("Новый")),
        (VIEWED, _("Просмотрено")),
        (CONTACTED, _("Связались")),
        (NOT_INTEREST, _("Не интересно")),
        (MADE, _("Изготовлено")),
        (SENT, _("Отправлено")),
    )

    name = models.CharField(_("first name"), max_length=70)
    phone = models.CharField(_("phone"), max_length=32, db_index=True)
    email = models.EmailField(_("email"), max_length=254, null=True, blank=True)
    comment = models.TextField(_("comment"), default="", blank=True)
    lang_code = models.CharField(_("lang code"), default="ru", blank=True, max_length=2)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    status = models.PositiveIntegerField(_("new status"), choices=STATUS, default=NEW)
    added = models.DateTimeField(_("added"), auto_now_add=True)

    class Meta:
        ordering = ("-added",)
        verbose_name = _("I want")
        verbose_name_plural = _("I want")

    def __str__(self):
        return u"%s" % self.name


class NovaPoshtaRegions(models.Model):
    description = models.TextField(_("city name"))
    ref = models.CharField(_("ref"), max_length=40, db_index=True)
    areasenter_ref = models.CharField(_("areasenter_ref"), max_length=40, db_index=True)


    class Meta:
        ordering = ("description",)
        verbose_name = _("Nova_Poshta_Cities")
        verbose_name_plural = _("Nova_Poshta_Cities")

    def __str__(self):
        return u"%s" % self.description


class NovaPoshtaCities(models.Model):
    description = models.TextField(_("city name"))
    ref = models.CharField(_("ref"), max_length=40, db_index=True)
    novaposhtaregions = models.ForeignKey(NovaPoshtaRegions, null=True, blank=True, on_delete=models.CASCADE)
    settlement_type_description = models.TextField(_("settlement type description"))
    settlement_type_description_ru = models.TextField(_("settlement type description ru"))
    area_description = models.TextField(_("area description"))
    area_description_ru = models.TextField(_("area description ru"))

    class Meta:
        ordering = ("description",)
        verbose_name = _("Nova_Poshta_Cities")
        verbose_name_plural = _("Nova_Poshta_Cities")

    def __str__(self):
        return u"%s" % self.description


class NovaPoshtaWarehouses(models.Model):
    description = models.TextField(_("warehouses name"))
    number = models.PositiveIntegerField(_("number"))
    ref = models.CharField(_("ref"), max_length=40, db_index=True)
    novaposhtacities = models.ForeignKey(NovaPoshtaCities, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ("description",)
        verbose_name = _("Nova_Poshta_Warehouses")
        verbose_name_plural = _("Nova_Poshta_Warehouses")

    def __str__(self):
        return u"%s" % self.description
