import re

from django import forms
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField

from .models import Order


class OrderForm(forms.ModelForm):
    phone = PhoneNumberField(region="RU", error_messages={"invalid": "Неверный формат номера."})

    class Meta:
        model = Order
        fields = ["bouquet", "name", "phone", "address", "delivery_time"]

        widgets = {
            "bouquet": forms.HiddenInput(),
            "delivery_time": forms.RadioSelect(attrs={"class": "order__form_radio"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get("name").strip()
        if len(name) <= 2:
            raise ValidationError("Имя слишком короткое.")
        if not re.match(r"^[a-zA-Zа-яА-ЯёЁ\s\-]+$", name):
            raise ValidationError("Имя должно содержать только буквы.")
        return name

    def clean_address(self):
        address = self.cleaned_data.get("address")
        if len(address) < 10:
            raise ValidationError("Введите полный адрес доставки.")
        return address
