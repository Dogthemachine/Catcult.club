from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, Submit

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from apps.orders.models import Orders


class FilterForm(forms.Form):
    delivery = forms.ChoiceField(label='', choices=settings.DELIVERY)
    payment = forms.ChoiceField(label='', choices=settings.PAYMENT)
    status = forms.ChoiceField(label='', choices=settings.ORDER_STATUS)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.add_input(Submit('submit', _(u'Filter')))

        super(FilterForm, self).__init__(*args, **kwargs)


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
