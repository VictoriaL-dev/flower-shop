from django.urls import path

from . import views

app_name = "consultations"

urlpatterns = [
    path("consult/", views.consult, name="consult"),
]
