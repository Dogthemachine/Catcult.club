from allauth.utils import get_user_model
from django_resized import ResizedImageField
from solo.models import SingletonModel

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.elephants.models import Items, Sets


class Comments(models.Model):
    items = models.ForeignKey(Items, blank=True, null=True)
    sets = models.ForeignKey(Sets, blank=True, null=True)
    user = models.ForeignKey(get_user_model())
    comment = models.TextField(_('description'), blank=True, default='')
    moderated = models.BooleanField(_('moderated'), default=False)
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        verbose_name = _('Comments')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return u'%s' % self.comment

    def get_replies(self):
        return Reply_to_comments.objects.filter(comments=self).order_by('-added')


class Reply_to_comments(models.Model):
    comments = models.ForeignKey(Comments)
    user = models.ForeignKey(get_user_model())
    reply = models.TextField(_('description'), blank=True, default='')
    moderated = models.BooleanField(_('moderated'), default=False)
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        verbose_name = _('Reply_to_comments')
        verbose_name_plural = _('Reply_to_comments')

    def __str__(self):
        return u'%s' % self.comments
