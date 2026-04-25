from django.core.exceptions import ValidationError
from django.db import models


class BouquetTag(models.Model):
    """Теги для категоризации букетов."""
    TAG_CATEGORIES = [
        ('event', 'Событие'),
        ('style', 'Стиль'),
        ('color', 'Цветовая гамма'),
        ('budget', 'Бюджет'),
        ('flower', 'Цветок'),
        ('other', 'Прочее'),
    ]

    name = models.CharField(max_length=100, unique=True, verbose_name="Название тега")
    category = models.CharField(
        max_length=20,
        choices=TAG_CATEGORIES,
        blank=True,
        null=True,
        verbose_name="Категория тега"
    )
    min_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Мин. цена",
    )
    max_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Макс. цена",
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name}"

    def clean(self):
        if self.category == "budget" and (self.min_price is None or self.max_price is None):
            raise ValidationError(
                "Для тегов категории «Бюджет» необходимо указать мин. и макс. цену."
            )


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
    tags = models.ManyToManyField(BouquetTag, blank=True, verbose_name="Теги")

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
    

class Quiz(models.Model):
    """Квиз."""
    title = models.CharField(max_length=255, verbose_name="Название квиза")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Квиз"
        verbose_name_plural = "Квизы"

    def __str__(self):
        return f"{self.title}"
    

class QuizQuestion(models.Model):
    """Один вопрос внутри квиза."""
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Квиз"
    )
    text = models.CharField(max_length=500, verbose_name="Текст вопроса")
    step_number = models.PositiveIntegerField(verbose_name="Номер шага")

    class Meta:
        verbose_name = "Вопрос квиза"
        verbose_name_plural = "Вопросы квиза"
        ordering = ["quiz", "step_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["quiz", "step_number"],
                name="unique_step_per_quiz",
            )
        ]

    def __str__(self):
        return f"[{self.quiz.title}] Шаг {self.step_number}: {self.text[:50]}"
    

class QuizAnswer(models.Model):
    """Вариант ответа на вопрос. При выборе добавляет теги пользователю."""
    question = models.ForeignKey(
        QuizQuestion,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Вопрос",
    )
    text = models.CharField(max_length=255, verbose_name="Текст ответа")
    tags = models.ManyToManyField(
        BouquetTag,
        blank=True,
        verbose_name="Теги, добавляемые при выборе",
    )

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"

    def __str__(self):
        return f"{self.question.text[:40]} -> {self.text}"
