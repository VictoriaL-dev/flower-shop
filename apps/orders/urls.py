from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("make-order/<int:bouquet_id>/", views.create_order, name="make-order"),
    path("order-payment", views.pay_order, name="order-payment")
]
