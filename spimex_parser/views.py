from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render # noqa: F401

from prices_analyzer.services.petroleum import (
    get_petroleums_from_products,
    get_products_from_trade_day,
    save_petroleums_to_db,
)
from spimex_parser.parser import fetch_trade_day, save_trade_day_to_db, get_date


def trade_day_to_db_view(request: HttpRequest) -> HttpResponse:
    raw_day = request.GET.get('day')
    if not raw_day:
        return HttpResponseBadRequest('Не задана дата')
    
    
    day = get_date(raw_day)
    

    trade_day = fetch_trade_day(day=day)
    products = get_products_from_trade_day(trade_day=trade_day)
    petroleums = get_petroleums_from_products(products=products)


    try:
        save_trade_day_to_db(trade_day)
        save_petroleums_to_db(petroleums)
        result = 'success'

    
    except (TypeError, ValueError) as e:
        result = f'Incorrect data format {e}'

    return HttpResponse(result)


