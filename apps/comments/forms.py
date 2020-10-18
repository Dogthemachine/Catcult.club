from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper


class CommentForm(forms.Form):
    item_id = forms.IntegerField(widget=forms.HiddenInput)
    set_id = forms.IntegerField(widget=forms.HiddenInput)
    comment = forms.CharField(
        label=_("Your comment"),
        max_length=1024,
        widget=forms.Textarea(attrs={"rows": 4}),
    )

    def __init__(self, *args, **kwargs):
        """
        Basic Crispy forms config.

        """
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_id = "cc-add-comment-form"
        self.helper.form_action = "comment/"

        super(CommentForm, self).__init__(*args, **kwargs)


class ReplayForm(forms.Form):
    comment_id = forms.IntegerField(widget=forms.HiddenInput)
    comment = forms.CharField(
        label=_("Your replay"),
        max_length=1024,
        widget=forms.Textarea(attrs={"rows": 4}),
    )

    def __init__(self, *args, **kwargs):
        """
        Basic Crispy forms config.

        """
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_id = "cc-add-replay-form"
        self.helper.form_action = "replay/"

        super(ReplayForm, self).__init__(*args, **kwargs)
