from django.urls import path
from .views import home_view  # Import the correct view function

urlpatterns = [
    path("", home_view, name="home"),  # Use the imported home_view function
]
