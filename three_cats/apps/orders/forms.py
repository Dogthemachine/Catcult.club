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


class CommentForm(forms.Form):
    comment = forms.CharField(label='', max_length=512, widget=forms.Textarea(attrs={'rows': 3, 'cols': 12}))

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.form_action = '.'
        self.helper.add_input(Submit('submit', _(u'Save')))

        super(CommentForm, self).__init__(*args, **kwargs)


class StatusesForm(forms.Form):
    name = forms.CharField(label='Name', max_length=64)
    phone = forms.CharField(label='Phone', max_length=32)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'cc-checkout-form'
        self.helper.form_action = '.'

        super(StatusesForm, self).__init__(*args, **kwargs)


class DeleteForm(forms.Form):
    name = forms.CharField(label='Name', max_length=64)
    phone = forms.CharField(label='Phone', max_length=32)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'cc-checkout-form'
        self.helper.form_action = '.'

        super(DeleteForm, self).__init__(*args, **kwargs)
