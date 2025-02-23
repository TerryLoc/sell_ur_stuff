from django.urls import path
from .views import market_list
from . import views

urlpatterns = [
    path("", market_list, name="market_list"),
]
