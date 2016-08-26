from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'apps.main_page.views.construction_page', name='construction'),
    url(r'^4321/$', 'apps.main_page.views.main_page', name='main_page'),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', 'apps.info.views.user_login', name='user_login'),
    url(r'^logout/$', 'apps.info.views.user_logout', name='user_logout'),

    url(r'^feedback/$', 'apps.info.views.feedback', name='feedback'),
    url(r'^contacts/$', 'apps.info.views.contacts', name='contacts'),

    url(r'^showcase/(?P<category_id>\d+)/(?P<fashion_id>\d+)/$', 'apps.elephants.views.showcase', name='showcase'),
    url(r'^item_details/(?P<id>\d+)/$', 'apps.elephants.views.item_details', name='item_details'),

    url(r'^balances/$', 'apps.moderation.views.balances', name='balances'),
    url(r'^advent/$', 'apps.moderation.views.advent', name='advent'),
    url(r'^correction/$', 'apps.moderation.views.correction', name='correction'),

    url(r'^order/(?P<id>\d+)/(?P<amount>\d+)/$', 'apps.elephants.views.elephants_order', name='elephants_order'),
    url(r'^feedback_order/(?P<id>\d+)/$', 'apps.info.views.feedback_order', name='feedback_order'),
    url(r'^cart/$', 'apps.elephants.views.cart', name='cart'),
    url(r'^cart_remove/(?P<id>\d+)/$', 'apps.elephants.views.cart_remove', name='cart_remove'),
    url(r'^checkout/$', 'apps.info.views.checkout', name='checkout'),
    url(r'^orders/$', 'apps.elephants.views.orders', name='orders_table'),
    url(r'^orders/(?P<status>\d+)/$', 'apps.elephants.views.orders', name='orders_table'),
    url(r'^orders/(?P<status>\d+)/(?P<id>\d+)/$', 'apps.elephants.views.orders', name='orders_table'),
    url(r'^order_position/$', 'apps.elephants.views.order_position', name='order_position'),

    url(r'^i18n/', include('django.conf.urls.i18n')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
