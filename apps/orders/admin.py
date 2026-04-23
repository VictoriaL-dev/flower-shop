from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "phone", "status", "delivery_time"]
    list_display_links = ["id", "name"]
    list_filter = ["status", "delivery_time", "created_at"]
    search_fields = ["name", "phone", "address", "payment_id"]
    list_editable = ["status"]
    readonly_fields = ["created_at", "payment_id"]
    list_per_page = 20

    fieldsets = (
        ("Данные клиента", {
            "fields": ["name", "phone", "address"]
        }),
        ("Детали заказа", {
            "fields": ["status", "delivery_time", "bouquet", "price", "comment"]
        }),
        ("Служебная информация", {
            "fields": ["created_at", "payment_id"],
            "classes": ["collapse"]
        })
    )
