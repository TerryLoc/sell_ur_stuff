from django.urls import path
from . import views

urlpatterns = [
    # Basic sale views
    path("", views.sales_list, name="sales_list"),
    path("<int:sale_id>/", views.sale_detail, name="sale_detail"),
    path("create/", views.sale_create, name="sale_create"),
    path("<int:sale_id>/edit/", views.sale_update, name="sale_update"),
    path("<int:sale_id>/delete/", views.sale_delete, name="sale_delete"),
    # Payment views for buying a product directly
    path("buy/<int:sale_id>/", views.buy_product, name="buy_product"),
    path("success/", views.payment_success, name="payment_success"),
    path("cancel/", views.payment_cancel, name="payment_cancel"),
    # Offer views for making and managing offers
    path("offer/<int:sale_id>/", views.make_offer, name="make_offer"),
    path("offer/<int:offer_id>/accept/", views.accept_offer, name="accept_offer"),
    path("offer/<int:offer_id>/reject/", views.reject_offer, name="reject_offer"),
    path(
        # URL where Stripe redirects users after a successful payment through the direct checkout flow
        "offer_payment_success/",
        views.offer_payment_success,
        name="offer_payment_success",
    ),
    path(
        "offer_payment_cancel/", views.offer_payment_cancel, name="offer_payment_cancel"
    ),
    # Counteroffer views
    path("offer/<int:offer_id>/counter/", views.counter_offer, name="counter_offer"),
    path(
        "offer/<int:offer_id>/respond/",
        views.respond_counter_offer,
        name="respond_counter_offer",
    ),
    # Payment views for accepting an
    path("offer/<int:offer_id>/pay/", views.pay_offer, name="pay_offer"),
    # Payment views for buying a product through an offer
    path("payment_result/", views.payment_result, name="payment_result"),
]
