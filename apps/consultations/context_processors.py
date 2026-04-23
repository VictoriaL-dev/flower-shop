from .forms import ConsultationForm


def consultation_form_processor(request):
    return {
        "consultation_form": ConsultationForm()
    }
