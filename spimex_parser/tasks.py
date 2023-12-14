# TODO crontab на 16:30 каждый день, кроме выходных
import datetime
from celery import shared_task
from celery.schedules import crontab
from petroleum_prices.celery import app
from typing import Any
from spimex_parser.parser import save_trade_day_petroleums_to_db
from prices_analyzer.services.create_prices import create_prices_for_all_depots_for_day

@shared_task
def get_trade_day_for_today() -> None:
    current_day = datetime.date.today()
    save_trade_day_petroleums_to_db(day=current_day)
    create_prices_for_all_depots_for_day(day=current_day)


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Any, **kwargs: dict) -> None:
    sender.add_periodic_task(
        crontab(hour=16, minute=30),
        get_trade_day_for_today.s(),
        name='save trade day data from spimex to db every day '
    )
