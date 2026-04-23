from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["bouquet", "name", "phone", "address", "delivery_time"]

        widgets = {
            "bouquet": forms.HiddenInput(),

            "name": forms.TextInput(attrs={
                "placeholder": "Введите имя",
                "class": "order__form_input"
            }),
            "phone": forms.TextInput(attrs={
                "placeholder": "+7 (999) 000 00 00",
                "class": "order__form_input"
            }),
            "address": forms.TextInput(attrs={
                "placeholder": "Адрес доставки",
                "class": "order__form_input"
            }),
            "delivery_time": forms.RadioSelect(attrs={
                "class": "order__form_radio"
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
