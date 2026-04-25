from django.apps import AppConfig


class BouquetsConfig(AppConfig):
    name = "apps.bouquets"

    def ready(self):
        from django.db.models.signals import post_save
        from .models import Bouquet
        from .signals import on_bouquet_save

        post_save.connect(on_bouquet_save, sender=Bouquet)
