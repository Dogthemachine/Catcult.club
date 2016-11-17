from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, Submit

from django import forms
from django.conf import settings
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _


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


class CheckoutForm(forms.Form):
    name = forms.CharField(label=_('Your name:'), max_length=64)
    phone = forms.CharField(label=_('Phone number:'))
    payment = forms.TypedChoiceField(label=_('Payment Method'), choices=lang(settings.PAYMENT), coerce=int, widget=forms.RadioSelect())
    delivery = forms.TypedChoiceField(label=_('Delivery Method'), choices=lang(settings.DELIVERY), coerce=int, widget=forms.RadioSelect())
    comment = forms.CharField(label=_('Your address:'), max_length=512)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'cc-checkout-form'
        self.helper.form_action = '.'

        super(CheckoutForm, self).__init__(*args, **kwargs)


class CommentForm(forms.Form):
    comment = forms.CharField(label=_('Comment'))

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'cc-comment-form'
        self.helper.form_action = '.'

        super(CommentForm, self).__init__(*args, **kwargs)

