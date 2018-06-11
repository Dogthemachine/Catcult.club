from django_resized import ResizedImageField
from solo.models import SingletonModel

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.elephants.models import Items


class Gallery(models.Model):
    name = models.CharField(_('name'), max_length=250, blank=True, default='')
    items = models.ForeignKey(Items, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    image = ResizedImageField(size=[2500, 2500], upload_to='photos/%Y/%m/%d')
    image_small = ResizedImageField(size=[300, 300], crop=['middle', 'center'], upload_to='small_photos/%Y/%m/%d', editable=False)
    description = models.TextField(_('description'), blank=True, default='')
    added = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        verbose_name = _('Gallery')
        verbose_name_plural = _('Gallery')

    def __str__(self):
        return u'%s' % self.name


    def save(self, *args, **kwargs):
        if not self.image._committed:
            self.image_small = self.image.file
        super().save(*args, **kwargs)
