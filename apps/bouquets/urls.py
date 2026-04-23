from django.urls import path

from . import views

app_name = "bouquets"

urlpatterns = [
    path("catalog/", views.catalog, name="catalog"),
    path("card/<int:bouquet_id>/", views.card, name="card"),
]
