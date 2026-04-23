from django import forms
from .models import ConsultationRequest


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = ConsultationRequest
        fields = ["name", "phone"]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Введите Имя",
                "required": True,
            }),
            "phone": forms.TextInput(attrs={
                "placeholder": "+ 7 (999) 000 00 00",
                "required": True,
            }),
        }
