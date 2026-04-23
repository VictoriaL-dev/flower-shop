from django.contrib import admin

from .models import ConsultationRequest


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "phone", "status", "created_at"]
    list_display_links = ["id", "name"]
    list_filter = ["status", "created_at"]
    search_fields = ["name", "phone"]
    list_editable = ["status"]
    readonly_fields = ["created_at"]
    list_per_page = 20
