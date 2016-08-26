from django.contrib.auth.models import User

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.elephants.models import Balance


class Corrections(models.Model):
    balance = models.ForeignKey(Balance)
    user = models.ForeignKey(User)
    amount = models.PositiveSmallIntegerField(_('amount'), default=0)
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        verbose_name = _('Corrections')
        verbose_name_plural = _('Corrections')

    def __unicode__(self):
        return u'%s' % self.added


class Advent_tmp(models.Model):
    balance = models.ForeignKey(Balance)
    user = models.ForeignKey(User)
    amount = models.PositiveSmallIntegerField(_('amount'), default=0)

    class Meta:
        verbose_name = _('Advent')
        verbose_name_plural = _('Advent')

    def __unicode__(self):
        return u'%s' % self.amount


class Advent(models.Model):
    balance = models.ForeignKey(Balance)
    user = models.ForeignKey(User)
    amount = models.PositiveSmallIntegerField(_('amount'), default=0)
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        verbose_name = _('Advent')
        verbose_name_plural = _('Advent')

    def __unicode__(self):
        return u'%s' % self.amount
