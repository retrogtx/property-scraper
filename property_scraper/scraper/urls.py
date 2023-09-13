from django.urls import path
from .views import scrape_view  # import view function

urlpatterns = [
    path("", scrape_view, name="scrape"),  # map view function to empty path
]
