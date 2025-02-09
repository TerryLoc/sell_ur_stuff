from django.urls import path
from . import views

urlpatterns = [
    path("", views.sales_list, name="sales_list"),  # This handles the sales list page
    path("create/", views.sale_create, name="sale_create"),  # Handle product creation
    path(
        "<int:id>/", views.sale_detail, name="sale_detail"
    ),  # Detail view for each product
]
