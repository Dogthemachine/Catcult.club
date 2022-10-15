from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.elephants.views import (
    showcase,
    item_details,
    item_set_details,
    stocks,
    i_want,
    artists,
)
from apps.info.views import user_login, user_logout, feedback, topic_view, contacts
from apps.main_page.views import main_page
from apps.gallery.views import (
    gallery,
    gallery_photo,
    gallery_photo_mod,
    gallery_photo_buy,
)
from apps.comments.views import (
    comment,
    replay,
    replay_activate,
    replay_deactivate,
    replay_delete,
    comment_activate,
    comment_deactivate,
    comment_delete,
    comments,
)
from apps.moderation.views import (
    balances,
    log,
    balances_update,
    export_balance,
    manage_orders,
    manage_order,
    delete_order_item,
    add_order_item,
    delete_order,
    check_orders,
    order_comment,
    order_delivery,
    j_order_info,
    j_order_delete,
    j_order_comment,
    j_order_delivery,
    j_order_payment,
    j_order_payment_delete,
    j_order_packed,
    stat_sale,
    stat_balance,
    stat_ending,
    stat_payment,
    manage_iwant,
    iwant_change_status,
    iwant_change_comment,
    manage_comments,
    comment_change_status,
    iwant_delete,
)
from apps.orders.views import (
    cart,
    cart_checkout,
    cart_remove,
    # liqpay_callback,
    wfp_callback,
    messages_off,
    cart_valuta,
    cart_plus,
    cart_warehouses,
    cart_cities,
)
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from apps.sitemap import sitemaps
from django.views.decorators.cache import cache_page

from apps.helpers import rozetka

urlpatterns = [
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots_file",
    ),
    path(
        "sitemap.xml",
        cache_page(3600)(sitemap),
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("accounts/", include("allauth.urls")),
    # url(r'^liqpay_callback/', liqpay_callback, name='liqpay_callback'),
    path("wfp_callback/", wfp_callback, name="wfp_callback"),
]

urlpatterns += (
    i18n_patterns(
        path("", showcase, name="main_page"),
        path("rozetka_DrStcK5.xml", rozetka, name="rozetka"),
        path("admin/", admin.site.urls),
        path("login/", user_login, name="user_login"),
        path("logout/", user_logout, name="user_logout"),
        # Info
        path("main/", main_page, name="main_info"),
        path("feedback/", feedback, name="feedback"),
        path("contacts/", contacts, {"topic": "contacts"}, name="contacts"),
        path("about/", topic_view, {"topic": "about_us"}, name="about_us"),
        path(
            "policies_privacy/",
            topic_view,
            {"topic": "privacy"},
            name="policies_privacy",
        ),
        path("policies_terms/", topic_view, {"topic": "terms"}, name="policies_terms"),
        # url(r'^partners/', topic_view, {'topic': 'partners'}, name='partners'),
        # Shop
        path("showcase/<int:category_id>/", showcase, name="showcase_cat"),
        path("showcase-artist/<int:artist_id>/", showcase, name="showcase_artist"),
        path(
            "showcase/<int:category_id>/<int:fashion_id>/",
            showcase,
            name="showcase_cat_fas",
        ),
        path("item/<int:id>/", item_details, name="item_details"),
        path("item-set/<int:id>/", item_set_details, name="item_set_details"),
        path("stocks/", stocks, name="stocks"),
        path("i-want/<int:id>/", i_want, name="i_want"),
        path("artists/", artists, name="artists"),
        # url(r'^stock/<id>/', stock_details, name='stock_details'),
        # Comments
        path("comment/", comment, name="comment"),
        path("comments/", comments, name="all_comments"),
        path("replay/", replay, name="replay"),
        path(
            "replay-activate/<int:comm_id>/",
            replay_activate,
            name="replay_activate",
        ),
        path(
            "replay-deactivate/<int:comm_id>/",
            replay_deactivate,
            name="replay_deactivate",
        ),
        path("replay-delete/<int:comm_id>/", replay_delete, name="replay_delete"),
        path(
            "comment-activate/<int:comm_id>/",
            comment_activate,
            name="comment_activate",
        ),
        path(
            "comment-deactivate/<int:comm_id>/",
            comment_deactivate,
            name="comment_deactivate",
        ),
        path("comment-delete/<int:comm_id>/", comment_delete, name="comment_delete"),
        # Moderator
        path("orders/", manage_orders, name="orders"),
        path("i-want-mod/", manage_iwant, name="i_want_mod"),
        path("comments-mod/", manage_comments, name="comments_mod"),
        path("orders/check/", check_orders, name="check_orders"),
        path("orders/<int:id>/", manage_order, name="manage_order"),
        path("orders/<int:id>/info/", j_order_info, name="order_info"),
        path("orders/<int:id>/delete/", j_order_delete, name="order_delete"),
        path("orders/<int:id>/comment/", j_order_comment, name="order_comment"),
        path("orders/<int:id>/delivery/", j_order_delivery, name="order_delivery"),
        path("orders/<int:id>/packed/", j_order_packed, name="order_packed"),
        path(
            "orders/<int:id>/delivery/reset/",
            j_order_delivery,
            {"reset": True},
            name="order_delivery_reset",
        ),
        path("orders/<int:id>/payment/", j_order_payment, name="order_payment"),
        path(
            "orders/payment/<int:id>/delete/",
            j_order_payment_delete,
            name="order_payment_delete",
        ),
        path("orders/delete/<int:id>/", delete_order, name="delete_order"),
        path(
            "orders/<int:id>/delete/<int:item_id>/",
            delete_order_item,
            name="delete_order_item",
        ),
        path(
            "orders/<int:id>/add/<int:balance_id>/",
            add_order_item,
            name="add_order_item",
        ),
        path("balances/", balances, name="balances"),
        path("balances/update/", balances_update, name="balances_update"),
        path("balances/download/", export_balance, name="export_balance"),
        path("log/", log, name="log"),
        path("order_info/<int:id>/", order_comment, name="order_payment"),
        path("order_comment/<int:id>/", order_comment, name="order_comment"),
        path("order_delivery/<int:id>/", order_comment, name="order_delivery"),
        path("order_payment/<int:id>/", order_comment, name="order_payment"),
        path("stat/payment/", stat_payment, name="stat_payment"),
        path(
            "i-want-mod/change/<int:order_id>/",
            iwant_change_status,
            name="iwant_change_status",
        ),
        path("i-want-mod/delete/<int:order_id>/", iwant_delete, name="iwant_delete"),
        path(
            "i-want-mod/change-comment/<int:order_id>/",
            iwant_change_comment,
            name="iwant_change_comment",
        ),
        path(
            "comments-mod/change/<int:comment_id>/",
            comment_change_status,
            name="comment_change_status",
        ),
        # Statistics
        path("stat/sale/", stat_sale, name="stat_sale"),
        path("stat/ending0/", stat_ending, {"rest": 0}, name="stat_ending_0"),
        path("stat/ending1/", stat_ending, {"rest": 1}, name="stat_ending_1"),
        path("stat/balance/", stat_balance, name="stat_balance"),
        # Gallery
        path("gallery/", gallery, name="gallery"),
        path("gallery/<int:id>/", gallery_photo, name="gallery_photo"),
        path("gallery/photo/<int:id>/", gallery_photo_mod, name="gallery_photo_mod"),
        path(
            "gallery/photo_buy/<int:id>/",
            gallery_photo_buy,
            name="gallery_photo_buy",
        ),
        # Orders
        path("messages_off/<int:id>/", messages_off, name="messages_off"),
        # Cart
        path("cart/", cart, name="cart"),
        path("cart/<int:id>/remove/", cart_remove, name="cart_remove"),
        path("cart/<int:id>/plus/", cart_plus, {"plus": True}, name="cart_plus"),
        path("cart/<int:id>/minus/", cart_plus, {"plus": False}, name="cart_minus"),
        path(
            "cart/<int:id>/remove_set/",
            cart_remove,
            {"set": True},
            name="cart_remove_set",
        ),
        path("cart/checkout/", cart_checkout, name="cart_checkout"),
        path("cart/valuta/", cart_valuta, name="cart_valuta"),
        path("success/", main_page, name="payment_success"),
        path("cart/<int:city_id>/<int:warehouse_id>/warehouses/", cart_warehouses, name="cart_warehouses"),
        path("cart/<int:region_id>/<int:city_id>/cities/", cart_cities, name="cart_cities"),
        path("select2/", include("django_select2.urls")),
        path("i18n/", include("django.conf.urls.i18n")),
        prefix_default_language=False,
    )
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
