from django.urls import path

from . import views

app_name = "bouquets"

urlpatterns = [
    path("catalog/", views.catalog, name="catalog"),
    path("card/<int:pk>/", views.card, name="card"),
]
