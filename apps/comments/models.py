from allauth.utils import get_user_model
from django_resized import ResizedImageField
from solo.models import SingletonModel
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache.utils import make_template_fragment_key
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.elephants.models import Items, Sets


class Comments(models.Model):
    NEW = 1
    VIEWED = 2
    ANSWERED = 3

    STATUS = (
        (NEW, _("Новый")),
        (VIEWED, _("Просмотрено")),
        (ANSWERED, _("Отвечено")),
    )

    items = models.ForeignKey(Items, on_delete=models.CASCADE, blank=True, null=True)
    sets = models.ForeignKey(Sets, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment = models.TextField(_("description"), blank=True, default="")
    moderated = models.BooleanField(_("moderated"), default=False)
    status = models.PositiveIntegerField(_("new status"), choices=STATUS, default=NEW)
    added = models.DateTimeField(_("added"), auto_now_add=True)

    class Meta:
        verbose_name = _("Comments")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return u"%s" % self.comment

    def get_replies(self):
        return Reply_to_comments.objects.filter(comments=self).order_by("-added")


class Reply_to_comments(models.Model):
    comments = models.ForeignKey(Comments, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reply = models.TextField(_("description"), blank=True, default="")
    moderated = models.BooleanField(_("moderated"), default=False)
    added = models.DateTimeField(_("added"), auto_now_add=True)

    class Meta:
        verbose_name = _("Reply_to_comments")
        verbose_name_plural = _("Reply_to_comments")

    def __str__(self):
        return u"%s" % self.comments


def template_cache_key(name, *args):
    return make_template_fragment_key(name, args)


@receiver(post_save, sender=Comments)
def delete_item_cache(sender, instance, **kwargs):
    item = instance.items
    cache.delete(template_cache_key("item_template", item.id))


@receiver(post_delete, sender=Comments)
def delete_item_cache(sender, instance, **kwargs):
    item = instance.items
    cache.delete(template_cache_key("item_template", item.id))
