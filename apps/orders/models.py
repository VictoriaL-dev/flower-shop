from django.db import models

from apps.bouquets.models import Bouquet

from phonenumber_field.modelfields import PhoneNumberField


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", "Новый"
        PAID = "PAID", "Оплачен"
        DELIVERING = "DELIVERING", "Доставляется"
        COMPLETED = "COMPLETED", "Завершен"
        CANCELLED = "CANCELLED", "Отменен"

    class DeliveryTimeSlots(models.TextChoices):
        ASAP = "ASAP", "Как можно скорее"
        T10_12 = "10-12", "с 10:00 до 12:00"
        T12_14 = "12-14", "с 12:00 до 14:00"
        T14_16 = "14-16", "с 14:00 до 16:00"
        T16_18 = "16-18", "с 16:00 до 18:00"
        T18_20 = "18-20", "с 18:00 до 20:00"

    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = PhoneNumberField(region="RU", db_index=True, verbose_name="Телефон")
    address = models.CharField(max_length=150, verbose_name="Адрес доставки")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Дата создания")
    comment = models.TextField(blank=True, verbose_name="Комментарий к заказу")
    bouquet = models.ForeignKey(
        Bouquet,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Букет"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена"
    )
    payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_index=True,
        verbose_name="ID платежа ЮKassa"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
        verbose_name="Статус заказа"
    )
    delivery_time = models.CharField(
        max_length=20,
        choices=DeliveryTimeSlots.choices,
        default=DeliveryTimeSlots.ASAP,
        db_index=True,
        verbose_name="Время доставки"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ №{self.id} ({self.get_status_display()})"
