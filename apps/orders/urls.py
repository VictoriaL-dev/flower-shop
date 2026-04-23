from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("make-order/<int:bouquet_id>/", views.create_order, name="make-order"),
    path("order-payment/", views.pay_order, name="order-payment"),
    path("webhook/", views.yookassa_webhook, name="webhook"),
    path("payment/success/", views.payment_success, name="payment-success"),
    path("payment/failure/", views.payment_failure, name="payment-failure"),
]
