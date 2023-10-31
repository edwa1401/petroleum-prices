from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

from spimex_parser.models import Contract, Section, TradeDay
from spimex_parser.parser import (
    convert_date,
    create_trade_day,
    delete_all_emty_values_from_raw_data,
    download_file_from_spimex,
    get_all_cell_values_from_sheet,
    get_date,
    get_url_to_spimex_data,
    read_spimex_file,
)
from spimex_parser.shemas import Contract_sh, TradeDay_sh


def save_contract(contract: Contract_sh) -> Contract:
    return Contract(
        code=contract.code,
        name=contract.code,
        base=contract.base,
        volume=contract.volume,
        amount=contract.amount,
        price_change_amount=contract.price_change_amount,
        price_change_ratio=contract.price_change_ratio,
        price_min=contract.price_min,
        price_avg=contract.price_avg,
        price_max=contract.price_max,
        price_market=contract.price_market,
        price_best_bid=contract.price_best_bid,
        price_best_call=contract.price_best_call,
        num_of_lots=contract.num_of_lots
    )


def save_trade_day_to_db(trade_day: TradeDay_sh) -> None:
    
    trade_day_db = TradeDay(day=trade_day.day)
    trade_day_db.save(force_insert=True)

    for section in trade_day.sections:
        section_db = Section(name=section.name, metric=section.metric)
        section_db.save(force_insert=True)
        for contract in section.contracts:
            contact_db = save_contract(contract)
            contact_db.save(force_insert=True)
        



def trade_day_to_db_view(request: HttpRequest) -> HttpResponse:
    raw_day = request.GET.get('day')
    if not raw_day:
        return HttpResponseBadRequest('Не задана дата')
    
    # day = get_date(raw_day)
    # converted_day = convert_date(day)
    url = get_url_to_spimex_data(date=raw_day)
    content = download_file_from_spimex(url)
    sheet = read_spimex_file(content)
    raw_data = get_all_cell_values_from_sheet(sheet)
    all_values = delete_all_emty_values_from_raw_data(raw_data)
    trade_day = create_trade_day(all_values)

    try:
        save_trade_day_to_db(trade_day)
        result = 'success'

    
    except (TypeError, ValueError) as e:
        result = f'Incorrect data format {e}'

    return HttpResponse(result)