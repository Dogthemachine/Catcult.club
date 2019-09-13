from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin

from apps.elephants.views import showcase, item_details, item_set_details, stocks, i_want
from apps.info.views import user_login, user_logout, feedback, topic_view, contacts
from apps.main_page.views import main_page
from apps.gallery.views import gallery, gallery_photo, gallery_photo_mod,  gallery_photo_buy
from apps.comments.views import comment, replay, replay_activate, replay_deactivate, replay_delete, \
    comment_activate, comment_deactivate, comment_delete, comments
from apps.moderation.views import balances, log, balances_update, export_balance, manage_orders, manage_order, \
    delete_order_item, add_order_item, delete_order, check_orders, order_comment, order_delivery, j_order_info, \
    j_order_delete, j_order_comment, j_order_delivery, j_order_payment, j_order_payment_delete, j_order_packed, \
    stat_sale, stat_ending, stat_payment
from apps.orders.views import cart, cart_checkout, cart_remove, liqpay_callback, wfp_callback, messages_off, cart_valuta
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from apps.sitemap import sitemaps
from django.views.decorators.cache import cache_page

from apps.helpers import rozetka

urlpatterns = [
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots_file'),
    url(r'^sitemap\.xml$', cache_page(3600)(sitemap), {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    url('accounts/', include('allauth.urls')),
    #url(r'^liqpay_callback/$', liqpay_callback, name='liqpay_callback'),
    url(r'^wfp_callback/$', wfp_callback, name='wfp_callback'),
]

urlpatterns += i18n_patterns(
    url(r'^$', showcase, name='main_page'),
    url(r'^rozetka_DrStcK5\.xml$', rozetka, name='rozetka'),

    url(r'^admin/', admin.site.urls),
    url(r'^login/$', user_login, name='user_login'),
    url(r'^logout/$', user_logout, name='user_logout'),

    # Info
    url(r'^main/$', main_page, name='main_info'),
    url(r'^feedback/$', feedback, name='feedback'),
    url(r'^contacts/$', contacts, {'topic': 'contacts'}, name='contacts'),
    url(r'^about/$', topic_view, {'topic': 'about_us'}, name='about_us'),
    url(r'^policies_privacy/$', topic_view, {'topic': 'privacy'}, name='policies_privacy'),
    url(r'^policies_terms/$', topic_view, {'topic': 'terms'}, name='policies_terms'),
    #url(r'^partners/$', topic_view, {'topic': 'partners'}, name='partners'),

    # Shop
    url(r'^showcase/(?P<category_id>\d+)/$', showcase, name='showcase_cat'),
    url(r'^showcase/(?P<category_id>\d+)/(?P<fashion_id>\d+)/$', showcase, name='showcase_cat_fas'),
    url(r'^item/(?P<id>\d+)/$', item_details, name='item_details'),
    url(r'^item-set/(?P<id>\d+)/$', item_set_details, name='item_set_details'),
    url(r'^stocks/$', stocks, name='stocks'),
    url(r'^i-want/(?P<id>\d+)/$', i_want, name='i_want'),
    #url(r'^stock/(?P<id>\d+)/$', stock_details, name='stock_details'),

    # Comments
    url(r'^comment/$', comment, name='comment'),
    url(r'^comments/$', comments, name='all_comments'),
    url(r'^replay/$', replay, name='replay'),
    url(r'^replay-activate/(?P<comm_id>\d+)/$', replay_activate, name='replay_activate'),
    url(r'^replay-deactivate/(?P<comm_id>\d+)/$', replay_deactivate, name='replay_deactivate'),
    url(r'^replay-delete/(?P<comm_id>\d+)/$', replay_delete, name='replay_delete'),
    url(r'^comment-activate/(?P<comm_id>\d+)/$', comment_activate, name='comment_activate'),
    url(r'^comment-deactivate/(?P<comm_id>\d+)/$', comment_deactivate, name='comment_deactivate'),
    url(r'^comment-delete/(?P<comm_id>\d+)/$', comment_delete, name='comment_delete'),

    # Moderator
    url(r'^orders/$', manage_orders, name='orders'),
    url(r'^orders/check/$', check_orders, name='check_orders'),
    url(r'^orders/(?P<id>\d+)/$', manage_order, name='manage_order'),
    url(r'^orders/(?P<id>\d+)/info/$', j_order_info, name='order_info'),
    url(r'^orders/(?P<id>\d+)/delete/$', j_order_delete, name='order_delete'),
    url(r'^orders/(?P<id>\d+)/comment/$', j_order_comment, name='order_comment'),
    url(r'^orders/(?P<id>\d+)/delivery/$', j_order_delivery, name='order_delivery'),
    url(r'^orders/(?P<id>\d+)/packed/$', j_order_packed, name='order_packed'),
    url(r'^orders/(?P<id>\d+)/delivery/reset/$', j_order_delivery, {'reset': True}, name='order_delivery_reset'),
    url(r'^orders/(?P<id>\d+)/payment/$', j_order_payment, name='order_payment'),
    url(r'^orders/payment/(?P<id>\d+)/delete/$', j_order_payment_delete, name='order_payment_delete'),
    url(r'^orders/delete/(?P<id>\d+)/$', delete_order, name='delete_order'),
    url(r'^orders/(?P<id>\d+)/delete/(?P<item_id>\d+)/$', delete_order_item, name='delete_order_item'),
    url(r'^orders/(?P<id>\d+)/add/(?P<balance_id>\d+)/$', add_order_item, name='add_order_item'),
    url(r'^balances/$', balances, name='balances'),
    url(r'^balances/update/$', balances_update, name='balances_update'),
    url(r'^balances/download/$', export_balance, name='export_balance'),
    url(r'^log/$', log, name='log'),
    url(r'^order_info/(?P<id>\d+)/$', order_comment, name='order_payment'),
    url(r'^order_comment/(?P<id>\d+)/$', order_comment, name='order_comment'),
    url(r'^order_delivery/(?P<id>\d+)/$', order_comment, name='order_delivery'),
    url(r'^order_payment/(?P<id>\d+)/$', order_comment, name='order_payment'),
    url(r'^stat/payment/$', stat_payment, name='stat_payment'),

    # Statistics
    url(r'^stat/sale/$', stat_sale, name='stat_sale'),
    url(r'^stat/ending0/$', stat_ending, {'rest': 0}, name='stat_ending_0'),
    url(r'^stat/ending1/$', stat_ending, {'rest': 1}, name='stat_ending_1'),

    # Gallery
    url(r'^gallery/$', gallery, name='gallery'),
    url(r'^gallery/(?P<id>\d+)/$', gallery_photo, name='gallery_photo'),
    url(r'^gallery/photo/(?P<id>\d+)/$', gallery_photo_mod, name='gallery_photo_mod'),
    url(r'^gallery/photo_buy/(?P<id>\d+)/$', gallery_photo_buy, name='gallery_photo_buy'),

    # Orders
    url(r'^messages_off/(?P<id>\d+)/$', messages_off, name='messages_off'),

    # Cart
    url(r'^cart/$', cart, name='cart'),
    url(r'^cart/(?P<id>\d+)/remove/$', cart_remove, name='cart_remove'),
    url(r'^cart/(?P<id>\d+)/remove_set/$', cart_remove, {'set': True }, name='cart_remove_set'),
    url(r'^cart/checkout/$', cart_checkout, name='cart_checkout'),
    url(r'^cart/valuta/$', cart_valuta, name='cart_valuta'),

    url(r'^success/$', main_page, name='payment_success'),
    url(r'^i18n/', include('django.conf.urls.i18n')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
