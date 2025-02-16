from django.urls import path
from . import views

urlpatterns = [
    path("", views.sales_list, name="sales_list"),
    path("<int:sale_id>/", views.sale_detail, name="sale_detail"),
    path("create/", views.sale_create, name="sale_create"),
    path("<int:sale_id>/edit/", views.sale_update, name="sale_update"),
    path("<int:sale_id>/delete/", views.sale_delete, name="sale_delete"),
]
