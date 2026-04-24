import json
import uuid

from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from yookassa import Configuration, Payment

from .forms import OrderForm
from .models import Order
from apps.bouquets.models import Bouquet

Configuration.configure(settings.YOOKASSA_SHOP_ID, settings.YOOKASSA_SECRET_KEY)


@transaction.atomic
def create_order(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, id=bouquet_id)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.bouquet = bouquet
            order.price = bouquet.price
            order.save()

            request.session["current_order_id"] = order.id
            return redirect("orders:order-payment")
    else:
        if "current_order_id" in request.session:
            del request.session["current_order_id"]
        form = OrderForm(initial={"bouquet": bouquet})

    return render(request, "orders/order.html", {
        "form": form,
        "bouquet": bouquet
    })


def pay_order(request):
    order_id = request.session.get("current_order_id")
    if not order_id:
        return redirect("pages:index")

    order = get_object_or_404(Order, id=order_id)

    if order.status != Order.Status.NEW:
        return redirect("pages:index")

    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": str(order.price),
            "currency": "RUB"
        },
        "capture": True,
        "confirmation": {
            "type": "redirect",
            "return_url": request.build_absolute_uri(
                reverse("orders:payment-success")
            )
        },
        "description": f"Заказ №{order.id}",
        "metadata": {
            "order_id": order.id
        }
    }, idempotence_key)

    order.payment_id = payment.id
    order.save()

    return redirect(payment.confirmation.confirmation_url)


@csrf_exempt
@require_POST
def yookassa_webhook(request):
    event = json.loads(request.body)
    payment = event.get("object", {})
    payment_id = payment.get("id")
    status = payment.get("status")

    try:
        order = Order.objects.get(payment_id=payment_id)
    except Order.DoesNotExist:
        return HttpResponse(status=404)

    if status == "succeeded":
        order.status = Order.Status.PAID
    elif status == "canceled":
        order.status = Order.Status.CANCELLED

    order.save(update_fields=["status"])
    return HttpResponse(status=200)


def payment_success(request):
    order_id = request.session.get("current_order_id")
    if order_id:
        order = Order.objects.filter(id=order_id).first()
        if order and order.status == Order.Status.PAID:
            del request.session["current_order_id"]
            return render(request, "orders/payment-success.html", {"order": order})
    return render(request, "orders/payment-success.html", {"order": None})


def payment_failure(request):
    return render(request, "orders/payment-failure.html")
