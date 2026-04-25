import logging

from django.db.models import Q

from .models import BouquetTag

logger = logging.getLogger(__name__)


def auto_assign_budget_tags(bouquet):
    budget_tags = BouquetTag.objects.filter(
        category="budget",
        min_price__isnull=False,
        max_price__isnull=False,
    )

    old_budget_tag_ids = set(
        bouquet.tags.filter(category="budget").values_list("id", flat=True)
    )
    new_budget_tag_ids = set()

    for tag in budget_tags:
        if tag.min_price <= bouquet.price <= tag.max_price:
            new_budget_tag_ids.add(tag.id)

    to_remove = old_budget_tag_ids - new_budget_tag_ids
    to_add = new_budget_tag_ids - old_budget_tag_ids

    if to_remove:
        bouquet.tags.remove(*to_remove)
    if to_add:
        bouquet.tags.add(*to_add)


def on_bouquet_save(sender, instance, created, **kwargs):
    auto_assign_budget_tags(instance)
