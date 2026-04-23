from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from .forms import OrderForm
from apps.bouquets.models import Bouquet


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
    pass
