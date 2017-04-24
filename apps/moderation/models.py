from django.db import models
from django.utils.translation import ugettext_lazy as _


class LastOrdersCheck(models.Model):
    datetime = models.DateTimeField(_('datetime'), auto_now=True)
