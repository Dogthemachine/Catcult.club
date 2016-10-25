from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin

from apps.elephants.views import showcase, item_details
from apps.info.views import user_login, user_logout, feedback, topic_view
from apps.main_page.views import main_page
from apps.moderation.views import balances, arrival, log, balances_update, export_balance, manage_orders, manage_order, delete_order_item, add_order_item, create_order, delete_order, check_orders
from apps.orders.views import cart, cart_checkout, cart_remove

admin.autodiscover()

urlpatterns = [
    url(r'^$', construction_page, name='construction'),
    url(r'^4321/$', main_page, name='main_page'),

    url(r'^admin/', admin.site.urls),
    url(r'^login/$', user_login, name='user_login'),
    url(r'^logout/$', user_logout, name='user_logout'),

    # Info
    url(r'^feedback/$', feedback, name='feedback'),
    url(r'^contacts/$', topic_view, {'topic': 'contacts'}, name='contacts'),
    url(r'^about/$', topic_view, {'topic': 'about_us'}, name='about_us'),
    url(r'^partners/$', topic_view, {'topic': 'partners'}, name='partners'),

    # Shop
    url(r'^showcase/$', showcase, name='showcase'),
    url(r'^showcase/(?P<category_id>\d+)/$', showcase, name='showcase_cat'),
    url(r'^showcase/(?P<category_id>\d+)/(?P<fashion_id>\d+)/$', showcase, name='showcase_cat_fas'),
    url(r'^item/(?P<id>\d+)/$', item_details, name='item_details'),

    # Moderator
    url(r'^orders/$', manage_orders, name='orders'),
    url(r'^orders/new/$', create_order, name='create_order'),
    url(r'^orders/check/$', check_orders, name='check_orders'),
    url(r'^orders/(?P<id>\d+)/$', manage_order, name='manage_order'),
    url(r'^orders/delete/(?P<id>\d+)/$', delete_order, name='delete_order'),
    url(r'^orders/(?P<id>\d+)/delete/(?P<item_id>\d+)/$', delete_order_item, name='delete_order_item'),
    url(r'^orders/(?P<id>\d+)/add/(?P<balance_id>\d+)/$', add_order_item, name='add_order_item'),
    url(r'^balances/$', balances, name='balances'),
    url(r'^balances/update/$', balances_update, {'arrival': False}, name='balances_update'),
    url(r'^balances/download/$', export_balance, name='export_balance'),
    url(r'^arrival/$', arrival, name='arrival'),
    url(r'^arrival/update/$', balances_update, {'arrival': True}, name='balances_update'),
    url(r'^log/$', log, name='log'),

    # Cart
    url(r'^cart/$', cart, name='cart'),
    url(r'^cart/(?P<id>\d+)/remove/$', cart_remove, name='cart_remove'),
    url(r'^cart/checkout/$', cart_checkout, name='cart_checkout'),

    url(r'^i18n/', include('django.conf.urls.i18n')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
