from django.urls import path
from .views import market_list
from . import views

urlpatterns = [
    path("", market_list, name="market_list"),
    path("buy/<int:product_id>/", views.buy_product, name="buy_product"),
    path("offer/<int:product_id>/", views.make_offer, name="make_offer"),
]
