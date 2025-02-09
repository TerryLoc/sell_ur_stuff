from django.urls import path
from .views import sales_list, sale_detail, sale_create, sale_update, sale_delete

urlpatterns = [
    path("", sales_list, name="sales_list"),
    path("<int:sale_id>/", sale_detail, name="sale_detail"),
    path("create/", sale_create, name="sale_create"),
    path("<int:sale_id>/edit/", sale_update, name="sale_update"),
    path("<int:sale_id>/delete/", sale_delete, name="sale_delete"),
]
