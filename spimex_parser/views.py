from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render  # noqa: F401

from prices_analyzer.services.petroleum import (
    get_petroleums_from_products,
    get_products_from_trade_day,
    save_petroleums_to_db,
)
from spimex_parser.parser import (
    check_trade_day_already_exists_in_db,
    fetch_trade_day,
    get_date,
    save_trade_day_to_db,
)


def trade_day_to_db_view(request: HttpRequest) -> HttpResponse:
    raw_day = request.GET.get('day')
    if not raw_day:
        return HttpResponseBadRequest('No day in request')
    
    
    day = get_date(raw_day)
    if check_trade_day_already_exists_in_db(day=day):
        return HttpResponse('trade day for {day} already saved'.format(day=day))

    trade_day = fetch_trade_day(day=day)
    products = get_products_from_trade_day(trade_day=trade_day)
    petroleums = get_petroleums_from_products(products=products)


    try:
        save_trade_day_to_db(trade_day)
        save_petroleums_to_db(petroleums)
        return HttpResponse('Trade day and petroleums for {day} successfully saved'.format(day=day))

    except (TypeError, ValueError) as e:
        return HttpResponse(f'Incorrect data format {e}')



