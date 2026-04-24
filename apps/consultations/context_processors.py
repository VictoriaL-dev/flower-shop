from .forms import ConsultationForm


def consultation_form_processor(request):
    form_data = request.session.pop("consultation_form_data", None)

    if form_data:
        form = ConsultationForm(form_data)
        form.is_valid()
    else:
        form = ConsultationForm()
    return {"consultation_form": form}
