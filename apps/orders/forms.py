from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, Submit

from django import forms
from django.conf import settings
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from apps.orders.models import Promo, Countris, Cart, NovaPoshtaCities, NovaPoshtaWarehouses
from apps.helpers import delivery_cost


def lang(t):
    """
    Actually making strings translatable.

    Variables: (tuple of tuples) `t`.

    Returns: list.

    """
    x = []
    for i in t:
        if i[1]:
            x.append((i[0], _(i[1])))
    return x


class CheckoutForm(forms.Form):

    # Build list of countries for dropdown list in form
    COUNTRIES = []

    name = forms.CharField(
        label=_("Your First name:"),
        widget=forms.TextInput(attrs={"placeholder": _("Enter your First name")}),
        max_length=64,
    )
    last_name = forms.CharField(
        label=_("Your Last name:"),
        widget=forms.TextInput(attrs={"placeholder": _("Enter your Last name")}),
        max_length=64,
    )
    phone = forms.CharField(
        label=_("Phone number:"),
        widget=forms.TextInput(attrs={"placeholder": "380001112233"}),
    )
    delivery = forms.TypedChoiceField(
        label=_("Delivery Method"),
        choices=lang(settings.DELIVERY),
        coerce=int,
        widget=forms.RadioSelect(),
    )
    city_np = forms.ModelChoiceField(
        label=_("Your city:"),
        queryset=NovaPoshtaCities.objects.exclude(description_ru='').exclude(description_uk=''),
        required=False,
    )
    warehouse_np = forms.ModelChoiceField(
        label=_("Nova Poshta warehouse:"),
        queryset=NovaPoshtaWarehouses.objects.all(),
        required=False,
    )
    shipping = forms.CharField(label=_("Your shipping address:"), max_length=512)
    email = forms.EmailField(label=_("Email address:"), required=False)
    payment = forms.TypedChoiceField(
        label=_("Payment Method"),
        choices=lang(settings.PAYMENT),
        coerce=int,
        widget=forms.RadioSelect(),
    )
    country = forms.ChoiceField(
        label=_("Country (cost of delivery)"), choices=COUNTRIES, required=False
    )
    promo = forms.CharField(label=_("Promo code (if any):"), required=False)

    def __init__(self, user, *args, **kwargs):
        self.cart = kwargs.pop("cart")
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_id = "cc-checkout-form"
        self.helper.form_action = "."

        self.user = user

        language = kwargs.pop('language')

        super(CheckoutForm, self).__init__(*args, **kwargs)

        per = False
        if self.user:
            per = self.user.has_perm("info.delete_info")

        c = []
        for p in settings.PAYMENT:
            if p[1] and (p[0] != 5 or per):
                c.append((p[0], _(p[1])))
        self.fields["payment"].choices = c

        c = []
        for p in settings.DELIVERY:
            # if p[1] and (p[0]!=2 or per):
            c.append((p[0], _(p[1])))
        self.fields["delivery"].choices = c

        self.fields["country"].choices = [
            (c.id, delivery_cost(c, self.cart)) for c in Countris.objects.all()
        ]

        # city_id = self.fields["city_np"].choices[0][0]
        # self.fields["warehouse_np"].choices = [
        #     (c.id, c.description_ru) for c in NovaPoshtaWarehouses.objects.filter(novaposhtacities__id=city_id) if c.description_ru
        # ]

    def clean(self):
        payment = self.cleaned_data.get("payment")
        delivery = self.cleaned_data.get("delivery")
        promo = self.cleaned_data.get("promo")
        email = self.cleaned_data.get("email")

        if payment != 5:
            if delivery and payment and delivery == 3 and payment < 3:
                msg = _(u"This payment method is not available when sending abroad.")
                self._errors["payment"] = self.error_class([msg])

            if promo:
                code = Promo.objects.filter(code=promo, used=False)
                if not code:
                    msg = _(
                        u"This code is not valid. Please enter a valid code or leave the field empty."
                    )
                    self._errors["promo"] = self.error_class([msg])

        if delivery and delivery == 3 and not email:
            msg = _(u"This field is required.")
            self._errors["email"] = self.error_class([msg])

        return self.cleaned_data


class CommentForm(forms.Form):
    comment = forms.CharField(label=_("Comment"))

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_id = "cc-comment-form"
        self.helper.form_action = "."

        super(CommentForm, self).__init__(*args, **kwargs)
