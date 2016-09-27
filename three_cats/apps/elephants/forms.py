from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, Submit

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Sizes, Balance


class AddToCartForm(forms.Form):
    size = forms.ModelChoiceField(label='Size', queryset=None, empty_label=None)
    quantity = forms.IntegerField(label='Quantity', min_value=1, max_value=10, initial=1)

    def __init__(self, *args, **kwargs):
        self.item = kwargs.pop('item')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.add_input(Submit('submit', _('Add to cart'), css_class="btn btn-success pull-right"))

        super(AddToCartForm, self).__init__(*args, **kwargs)

        self.fields['size'].queryset = Sizes.objects.select_related().filter(balance__item=self.item, balance__amount__gt=0)

    def clean_quantity(self, *args, **kwargs):
        balance = Balance.objects.get(size=self.cleaned_data['size'], item=self.item)
        if self.cleaned_data['quantity'] > balance.amount:
            raise forms.ValidationError(
                _('Sorry, these quantities are unavailable. Please choose another quantity.')
            )
        return self.cleaned_data['quantity']
