from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext


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


class ContactForm(forms.Form):
    name = forms.CharField(label=_('Name'), max_length=70, widget=forms.TextInput(attrs={'class': 'span9'}))
    phone = forms.CharField(label=_('Phone'), max_length=40, required=False, widget=forms.TextInput(attrs={'class': 'span9'}))
    email = forms.EmailField(label=_('Email'), max_length=40, required=False, widget=forms.TextInput(attrs={'class': 'span9'}))
    message = forms.CharField(label=_('Message'), max_length=1000, widget=forms.Textarea(attrs={'rows': 4, 'class': 'span9'}))

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.add_input(Submit('submit', ugettext(u'Send the message')))

        super(ContactForm, self).__init__(*args, **kwargs)


class LoginForm(forms.Form):
    login = forms.CharField(label=_('Login'), widget=forms.TextInput(attrs={'class': 'span4'}))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class': 'span4'}))

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.add_input(Submit('submit', _(u'Log in')))

        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        Extend clean() for:
        1. check if submitted user/password pair exists,
        2. check if user is not blocked.

        """
        data = self.cleaned_data
        login = data.get('login')
        password = data.get('password')

        if login and password:
            self.user = authenticate(username=login, password=password)
            if self.user is None:
                # If no user was found - raise a general error
                msg = _(u'Entered password does not ' +
                        u'correspont to entered login.')
                raise forms.ValidationError(msg)
            if not self.user.is_active:
                # ... also raise it when the user is blocked.
                msg = _(u'User is blocked. If you have ' +
                        u'any questions please contact us.')
                raise forms.ValidationError(msg)

        return data
