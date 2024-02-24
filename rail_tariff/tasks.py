from celery import shared_task

from prices_analyzer.models import Depot
from rail_tariff.services.create_rail_tariff import get_rail_tariffs_for_depot


@shared_task
def get_tariffs_for_all_depots() -> None:
    depots_id = Depot.objects.all().values_list('pk', flat=True)
    for depot_id in depots_id:
        get_rail_tariffs_for_depot(int(depot_id))


@shared_task
def get_tariffs_for_depot(depot_id: int) -> None:
    get_rail_tariffs_for_depot(depot_id=depot_id)
    

# TODO Таска в таком виде не нужна, должна сразу вызываться при создании depot,
# Затем в celery должна быть create or update (сейчас get or create) периодически (тарифы 
# индексируются обычно раз в полгода, но можно уточнять раз в месяц)

