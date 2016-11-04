from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, Submit

from django import forms
from django.conf import settings
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from apps.orders.models import Orders


def lang(t):
    """
    Actually making strings translatable.

    Variables: (tuple of tuples) `t`.

    Returns: list.

    """
    x = []
    for i in t:
        x.append((i[0], ugettext(i[1])))
    return x


class FilterForm(forms.Form):
    delivery = forms.ChoiceField(label='', choices=lang(settings.DELIVERY))
    payment = forms.ChoiceField(label='', choices=lang(settings.PAYMENT))

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.add_input(Submit('submit', _(u'Filter')))

        super(FilterForm, self).__init__(*args, **kwargs)


class CommentForm(forms.Form):
    comment = forms.CharField(label=_('Comment'), max_length=1024, required=False, widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'cc-order-comment-form'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'

        super(CommentForm, self).__init__(*args, **kwargs)


class DeliveryForm(forms.Form):
    delivery = forms.TypedChoiceField(label=_('Delivery'), choices=lang(settings.DELIVERY), coerce=int)
    ttn = forms.IntegerField(label=_('TTN'), required=False)
    date = forms.DateField(label=_('Date of delivery'), input_formats=['%d.%m.%Y'], required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'cc-order-delivery-form'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'

        super(DeliveryForm, self).__init__(*args, **kwargs)


class PaymentForm(forms.Form):
    amount = forms.IntegerField(label=_('Amount'))
    comment = forms.CharField(label=_('Comment'), max_length=512, required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'cc-order-payment-form'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'

        super(PaymentForm, self).__init__(*args, **kwargs)


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.add_input(Submit('submit', _(u'Save')))

        super(OrderForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Orders
        exclude = ['added']
