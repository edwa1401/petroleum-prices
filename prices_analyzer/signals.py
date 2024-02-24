import logging
from typing import Any, Type

from django.db.models.signals import post_save
from django.dispatch import receiver

from prices_analyzer.models import Depot
from rail_tariff.tasks import get_tariffs_for_depot

logger = logging.getLogger(__name__)
 
@receiver(post_save, sender=Depot) 
def get_rail_tariffs_for_created_depot(
    sender: Type[Depot],
    instance: Depot,
    created: bool,
    **kwargs: Any) -> None:

    if created:
        depot_id = instance.pk
        logger.info('depot_id=%s', depot_id)
        get_tariffs_for_depot.delay(depot_id=depot_id)

