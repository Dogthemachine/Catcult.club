from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, Submit

from django import forms
from django.utils.translation import ugettext_lazy as _


class CheckoutForm(forms.Form):
    name = forms.CharField(label='Name', max_length=64)
    phone = forms.CharField(label='Phone', max_length=32)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'cc-checkout-form'
        self.helper.form_action = '.'

        super(CheckoutForm, self).__init__(*args, **kwargs)
