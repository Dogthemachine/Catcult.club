from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, Submit, Div, Field

from django import forms
from django.forms import formset_factory
from django.utils.translation import ugettext_lazy as _

from .models import Sizes, Balance, Items


class AddToCartForm(forms.Form):
    size = forms.ModelChoiceField(label=_('Size'), queryset=None, empty_label=None, widget=forms.RadioSelect(),
                                  error_messages={'required': _('* Please choose a size'),
                                                  'invalid': _('* Please choose another size')})
    quantity = forms.IntegerField(label=_('Quantity'), min_value=1, max_value=10, initial=1)

    def __init__(self, *args, **kwargs):
        self.item = kwargs.pop('item')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.layout = Layout(
            Div(Field('size', css_class='form-tooltip', data_title=_('Size'), template='elephants/size_field.html')),
            Div(Field('quantity', data_title=_('Quantity'))),
            Div(Submit('submit', _('Add to cart'), template='elephants/button_field.html'))
        )

        super(AddToCartForm, self).__init__(*args, **kwargs)

        self.fields['size'].queryset = Sizes.objects.select_related().filter(balance__item=self.item, balance__amount__gt=0)

    def clean_quantity(self, *args, **kwargs):
        if self.cleaned_data.get('size', None):
            balance = Balance.objects.get(size=self.cleaned_data['size'], item=self.item)
            if self.cleaned_data['quantity'] > balance.amount:
                raise forms.ValidationError(
                    _('Sorry, these quantities are unavailable. Please choose another quantity.')
                )
            return self.cleaned_data['quantity']


class SetSizesForm(forms.Form):
    quantity = forms.IntegerField(label=_('Quantity'), min_value=1, max_value=10, initial=1)

    def __init__(self, *args, **kwargs):
        self.set = kwargs.pop('set')
        self.items_count = self.set.items.count()
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.layout = Layout(
            Div(Field('quantity', data_title=_('Quantity'))),
            Div(Submit('submit', _('Add to cart'), template='elephants/button_field.html'))
        )

        super(SetSizesForm, self).__init__(*args, **kwargs)

        for i, item in enumerate(self.set.items.all()):
            self.fields['item_%s' % i] = forms.ModelChoiceField(label=_('Size'), queryset=None, empty_label=None, widget=forms.RadioSelect(),
                                                                error_messages={'required': _('* Please choose a size'),
                                                                                'invalid': _('* Please choose another size')})
            self.fields['item_%s' % i].queryset = Sizes.objects.select_related().filter(balance__item=item, balance__amount__gt=0)
            self.fields['item_%s' % i].item = item
            self.helper.layout.insert(i, Div(Field('item_%s' % i, css_class='form-tooltip', data_title=_('Size'), template='elephants/set_size_field.html')))

    def clean(self, *args, **kwargs):
        for name, value in self.cleaned_data.items():
            if name.startswith('item_'):
                balance = Balance.objects.get(size=self.cleaned_data[name], item=self.fields[name].item.id)

                if self.cleaned_data['quantity'] > balance.amount:
                    raise forms.ValidationError(
                        _('Sorry, these quantities are unavailable. Please choose another quantity.')
                    )

        return self.cleaned_data