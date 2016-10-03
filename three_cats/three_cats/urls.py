from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin

from apps.main_page.views import construction_page, main_page
from apps.info.views import user_login, user_logout, feedback, contacts, about, partners, feedback_order, checkout
from apps.elephants.views import showcase, item_details
from apps.moderation.views import balances, arrival, log, balances_update
from apps.orders.views import cart, cart_checkout, orders, order_position, elephants_order, cart_remove

admin.autodiscover()

urlpatterns = [
    #url(r'^$', construction_page, name='construction'),
    url(r'^$', main_page, name='main_page'),

    url(r'^admin/', admin.site.urls),
    url(r'^login/$', user_login, name='user_login'),
    url(r'^logout/$', user_logout, name='user_logout'),

    # Store
    url(r'^feedback/$', feedback, name='feedback'),
    url(r'^contacts/$', contacts, name='contacts'),
    url(r'^about/$', about, name='about_us'),
    url(r'^partners/$', partners, name='partners'),

    # Shop
    url(r'^showcase/$', showcase, name='showcase'),
    url(r'^showcase/(?P<category_id>\d+)/$', showcase, name='showcase_cat'),
    url(r'^showcase/(?P<category_id>\d+)/(?P<fashion_id>\d+)/$', showcase, name='showcase_cat_fas'),
    url(r'^item/(?P<id>\d+)/$', item_details, name='item_details'),

    # Moderator
    url(r'^check_orders/$', balances, name='orders'),
    url(r'^make_order/$', balances, name='make_an_order'),
    url(r'^balances/$', balances, name='balances'), #done
    url(r'^balances/update/$', balances_update, name='balances_update'), #done
    url(r'^arrival/$', arrival, name='arrival'), #done
    url(r'^arrival/update/$', balances_update, {'arrival': True}, name='balances_update'), #done
    url(r'^log/$', log, name='log'), #done

    # Orders
    url(r'^cart/$', cart, name='cart'),
    url(r'^cart/(?P<id>\d+)/remove/$', cart_remove, name='cart_remove'),
    url(r'^cart/checkout/$', cart_checkout, name='cart_checkout'),
    url(r'^orders/$', orders, name='all_orders'),
    url(r'^orders/(?P<status>\d+)/$', orders, name='orders_status'),
    url(r'^order_position/(?P<id>\d+)/$', order_position, name='order_position'),
    url(r'^order/(?P<id>\d+)/$', elephants_order, name='elephants_order'),
    url(r'^feedback_order/(?P<id>\d+)/$', feedback_order, name='feedback_order'),
    url(r'^checkout/$', checkout, name='checkout'),


    url(r'^i18n/', include('django.conf.urls.i18n')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
