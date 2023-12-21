from typing import Any

from celery import shared_task
from celery.schedules import crontab

from petroleum_prices.tasks import app
from prices_analyzer.models import Depot
from rail_tariff.services.create_rail_tariff import get_rail_tariffs_for_depot


@shared_task
def get_tariffs_for_all_depots() -> None:
    depots_id = Depot.objects.all().values_list('pk', flat=True)
    for depot_id in depots_id:
        get_rail_tariffs_for_depot(int(depot_id))

# TODO Таска в таком виде не нужна, должна сразу вызываться при создании depot,
# Затем в celery должна быть create or update (сейчас get or create) периодически (тарифы 
# индексируются обычно раз в полгода, но можно уточнять раз в месяц)
        
# TODO после этого сразу должна вызываться create prices, для этого depot
# для petroleum-s за все дни, которые есть в базе 

@app.on_after_configure.connect
def setup_periodic_tasks(sender: Any, **kwargs: dict) -> None:
    sender.add_periodic_task(
        crontab(hour=13, minute=29),
        get_tariffs_for_all_depots.s(),
        name='get_rail_tariffs_for all depots for 13:10 every day'
    )

