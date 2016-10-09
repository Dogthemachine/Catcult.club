from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, Submit

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


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
    delivery = forms.ChoiceField(label='', choices=settings.DELIVERY)
    payment = forms.ChoiceField(label='', choices=settings.PAYMENT)
    status = forms.ChoiceField(label='', choices=settings.ORDER_STATUS)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.form_action = '.'
        self.helper.add_input(Submit('submit', _(u'Update')))

        super(StatusesForm, self).__init__(*args, **kwargs)


class DeleteForm(forms.Form):
    confirm = forms.BooleanField(label='')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.form_action = '.'
        self.helper.add_input(Submit('submit', _(u'Delete')))

        super(DeleteForm, self).__init__(*args, **kwargs)
