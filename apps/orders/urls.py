from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("make-order/", views.order, name="make-order"),
    path("payment/", views.order_step, name="payment")
]
