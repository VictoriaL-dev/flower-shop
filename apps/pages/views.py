from django.shortcuts import render

from apps.bouquets.models import Bouquet


def index(request):
    recommended_bouquets = Bouquet.objects.filter(is_available=True)[:3]
    return render(request, "index.html", {"bouquets": recommended_bouquets})


def consultation(request):
    return render(request, "consultation.html")


def order(request):
    return render(request, "order.html")


def order_step(request):
    return render(request, "order-step.html")


def quiz(request):
    return render(request, "quiz.html")


def quiz_step(request):
    return render(request, "quiz-step.html")


def quiz_result(request):
    return render(request, "result.html")
