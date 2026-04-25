import logging

from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import ConsultationForm

logger = logging.getLogger(__name__)


def consult(request):
    """Process applications from consultation.html."""
    if request.method == "POST":
        form = ConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Спасибо! Мы скоро с вами свяжемся.")
            return redirect("consultations:main-consultation-page")
    else:
        form = ConsultationForm()

    return render(request, "consultations/consultation.html", context={
        "form": form
    })


def handle_consultation_request(request):
    """Process applications from _consultation.html."""
    next_url = request.POST.get("next")

    if not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
        next_url = "/"

    if request.method == "POST":
        form = ConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Спасибо! Мы скоро с вами свяжемся.")
            return redirect(next_url)
        else:
            logger.warning("Invalid consultation form submitted")
            request.session["consultation_form_data"] = request.POST
            return redirect(next_url)
    return redirect(next_url)
