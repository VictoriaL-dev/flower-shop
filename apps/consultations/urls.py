from django.urls import path

from . import views

app_name = "consultations"

urlpatterns = [
    path("consult/", views.consult, name="main-consultation-page"),
    path("send-request/", views.handle_consultation_request, name="consultation-form"),
]
