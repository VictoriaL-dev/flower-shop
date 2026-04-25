from django.core.management.base import BaseCommand

from apps.bouquets.models import Bouquet
from apps.bouquets.signals import auto_assign_budget_tags


class Command(BaseCommand):
    help = "Auto-assign budget tags to all bouquets based on their price"

    def handle(self, *args, **options):
        bouquets = Bouquet.objects.all()
        total = bouquets.count()
        updated = 0

        for bouquet in bouquets:
            tag_count_before = bouquet.tags.filter(category="budget").count()
            auto_assign_budget_tags(bouquet)
            tag_count_after = bouquet.tags.filter(category="budget").count()
            if tag_count_before != tag_count_after:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Processed {total} bouquets, updated {updated}"
            )
        )
