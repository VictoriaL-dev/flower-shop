from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Flower, BouquetFlower, Bouquet, Supply, BouquetSupply


class BouquetFlowerInline(admin.TabularInline):
    model = BouquetFlower
    extra = 1


class BouquetSupplyInline(admin.TabularInline):
    model = BouquetSupply
    extra = 1


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ["get_image", "title", "price", "is_available"]
    list_display_links = ["get_image", "title"]
    list_filter = ["is_available", "flowers"]
    search_fields = ["title", "description", "flowers__name", "supplies__name"]
    exclude = ["flowers", "supplies"]
    inlines = [BouquetFlowerInline, BouquetSupplyInline]

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="75" style="border-radius: 5px;" />')
        return "Нет фото"

    get_image.short_description = "Превью"


@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    pass


@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    pass
