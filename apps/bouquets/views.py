from django.shortcuts import render, get_object_or_404

from apps.bouquets.models import Bouquet


def catalog(request):
    context = {"bouquets": Bouquet.objects.filter(is_available=True)}
    return render(request, "bouquets/catalog.html", context)


def card(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, pk=bouquet_id)
    return render(request, "bouquets/card.html", {"bouquet": bouquet})
