from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.elephants.models import Items, Sets


class ItemsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1
    protocol = 'https'
    i18n = True

    def items(self):
        return Items.objects.all()

    def lastmod(self, obj):
        return obj.added

    def location(self, obj):
        return reverse('item_details', args=(obj.id,))


class SetsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1
    protocol = 'https'
    i18n = True

    def items(self):
        return Sets.objects.all()

    def lastmod(self, obj):
        return obj.added

    def location(self, obj):
        return reverse('item_set_details', args=(obj.id,))


class StaticSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1
    protocol = 'https'
    i18n = True

    def items(self):
        return ['main_info', 'contacts', 'about_us', 'stocks']

    def location(self, item):
        return reverse(item)


sitemaps = {
    'items': ItemsSitemap,
    'sets': SetsSitemap,
    'static': StaticSitemap,
}
