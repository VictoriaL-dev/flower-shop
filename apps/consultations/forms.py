import re

from django import forms
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField

from .models import ConsultationRequest


class ConsultationForm(forms.ModelForm):
    phone = PhoneNumberField(region="RU", error_messages={"invalid": "Неверный формат номера."})

    class Meta:
        model = ConsultationRequest
        fields = ["name", "phone"]

    def clean_name(self):
        name = self.cleaned_data.get("name").strip()
        if len(name) <= 2:
            raise ValidationError("Имя слишком короткое.")
        if not re.match(r"^[a-zA-Zа-яА-ЯёЁ\s\-]+$", name):
            raise ValidationError("Имя должно содержать только буквы.")
        return name
