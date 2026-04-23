from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class ConsultationRequest(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новая"
        PROCESSED = "processed", "Обработана"
        CANCELLED = "cancelled", "Отменена"

    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = PhoneNumberField(region="RU", db_index=True, verbose_name="Телефон")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Дата заявки")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
        verbose_name="Статус"
    )

    class Meta:
        verbose_name = "Заявка на консультацию"
        verbose_name_plural = "Заявки на консультации"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заявка №{self.id} ({self.get_status_display()})"
