from django.db import models


class Flower(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название цветка")

    class Meta:
        verbose_name = "Цветок"
        verbose_name_plural = "Цветы"

    def __str__(self):
        return self.name


class Supply(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Наименование")

    class Meta:
        verbose_name = "Дополнение"
        verbose_name_plural = "Дополнения"

    def __str__(self):
        return self.name


class Bouquet(models.Model):
    image = models.ImageField(upload_to="bouquets/", verbose_name="Фото букета")
    title = models.CharField(max_length=255, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    is_available = models.BooleanField(default=True, verbose_name="В наличии")
    height = models.PositiveIntegerField(verbose_name="Высота (см)")
    width = models.PositiveIntegerField(verbose_name="Ширина (см)")
    flowers = models.ManyToManyField(Flower, through="BouquetFlower", verbose_name="Состав")
    supplies = models.ManyToManyField(Supply, through="BouquetSupply", verbose_name="Дополнения")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Букет"
        verbose_name_plural = "Букеты"

    def __str__(self):
        return self.title


class BouquetFlower(models.Model):
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, verbose_name="Цветок")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество (шт)")

    class Meta:
        verbose_name = "Цветок в букете"
        verbose_name_plural = "Состав букета"

    def __str__(self):
        return f"{self.flower.name} ({self.quantity} шт.)"


class BouquetSupply(models.Model):
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE)
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, verbose_name="Дополнение")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Дополнение для букета"
        verbose_name_plural = "Дополнения для букета"

    def __str__(self):
        return f"{self.supply.name} — {self.quantity} шт."
