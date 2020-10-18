from django.db import models
from django.utils.translation import gettext_lazy as _


class LastOrdersCheck(models.Model):
    datetime = models.DateTimeField(_("datetime"), auto_now=True)
