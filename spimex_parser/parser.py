from datetime import date, datetime
from typing import Any

import requests
import xlrd
from xlrd import sheet
from spimex_parser.models import Contract, Section, TradeDay

from spimex_parser.shemas import ContractSchema, SectionSchema, TradeDaySchema


def get_date(date: str) -> date:
    return datetime.date(datetime.strptime(date, '%Y-%m-%d'))


class DateValidationError(Exception):
    def __init__(self, message: str='No tradings in holidays') -> None:
        self.message = message
        super().__init__(self.message)


def validate_date(date: date) -> str:
    if date.weekday() == 5 or date.weekday() == 6:
        raise DateValidationError
    if len(str(date.day)) == 1:
        day = '0' + str(date.day)
    else:
        day = str(date.day)
    if len(str(date.month)) == 1:
        month = '0' + str(date.month)
    else:
        month = str(date.month)
    return str(date.year) + month + day


def get_url_to_spimex_data(date: str) -> str:

    URL_TRADINGS_START  = 'https://spimex.com/upload/reports/oil_xls/oil_xls_'
    URL_TRADINGS_END = '162000.xls'
    return '{}{}{}'.format(URL_TRADINGS_START, date, URL_TRADINGS_END)


def download_file_from_spimex(url: str) -> bytes:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        raise
    return response.content


def read_spimex_file(content: bytes) -> sheet.Sheet:
    workbook = xlrd.open_workbook(file_contents=content)
    return workbook.sheet_by_index(0)


def get_all_cell_values_from_sheet(sheet: sheet.Sheet) -> list[str]:
    all_raw_data = []
    for row in range(sheet.nrows):
        for column in range(sheet.ncols):
            all_raw_data.append(sheet.cell_value(row, column))
    return all_raw_data


def delete_all_emty_values_from_raw_data(raw_data: list[str]) -> list[str]:
    return [value for value in raw_data if value != '']


def get_indexes_for_search_value(all_values: list[str], search_value: str) -> list[int]:
    return [value for value in range(len(all_values)) if all_values[value].startswith(search_value)]


def extract_value_from_string(raw_string: str, prefix: str) -> str:
    if prefix in raw_string:
        return raw_string[len(prefix):len(raw_string)]
    else:
        return raw_string
    
def get_searched_string_from_all_values(
        all_values: list[str], search_value: str, prefix: str
        ) -> list[str]:
    indexes = get_indexes_for_search_value(all_values, search_value)
    return [
        extract_value_from_string(
            all_values[index], prefix
            ) for index in indexes if extract_value_from_string(
                all_values[index], prefix
                )
        ]


def fetch_day(all_values: list[str]) -> date:
    search_value ='Дата торгов: '
    prefix = search_value
    days_str = get_searched_string_from_all_values(
        all_values, search_value=search_value, prefix=prefix
        )
    days = [datetime.strptime(day_str, '%d.%m.%Y') for day_str in days_str]
    return datetime.date(days[0])


def convert_empty_strings_to_none(string: str) -> Any:
    return None if string == '-' else string


def convert_empty_values_to_zero(string: str) -> Any:
    return '0' if string == '-' else string


def get_sections_indexes(all_values: list[str]) -> list[list[int]]:
    start_section_indexes = get_indexes_for_search_value(all_values, search_value='Лучший\nспрос')
    end_section_indexes = get_indexes_for_search_value(all_values, search_value='Итого:')
    sections_indexes = []
    for sections_index in range(len(start_section_indexes)):
        sections_indexes.append(
            [start_section_indexes[sections_index] + 1, end_section_indexes[sections_index]]
            )
    return sections_indexes


def get_raw_sections(all_values: list[str], sections_indexes: list[list[int]]) -> list[list[str]]:
    return [
        all_values[section_indexes[0]:section_indexes[1]] for section_indexes in sections_indexes
        ]


def get_contracts_from_section(section: list[str]) -> list[ContractSchema]:
    NUM_COLUMNS_IN_SECTION = 14
    start_index = 0
    end_index = NUM_COLUMNS_IN_SECTION
    num_of_contracts_in_section = len(section) // NUM_COLUMNS_IN_SECTION
    contracts = []
    for _ in range(num_of_contracts_in_section):
        contract = section[start_index:end_index]
        start_index = end_index
        end_index = end_index + NUM_COLUMNS_IN_SECTION
        contracts.append(convert_contract(contract))
    return contracts


def convert_contract(contract: list[str]) -> ContractSchema:
    return ContractSchema(
        code=convert_empty_strings_to_none(contract[-14]),
        name=convert_empty_strings_to_none(contract[-13]),
        base=convert_empty_strings_to_none(contract[-12]),
        volume=convert_empty_values_to_zero(contract[-11]),
        amount=convert_empty_values_to_zero(contract[-10]),
        price_change_amount=convert_empty_strings_to_none(contract[-9]),
        price_change_ratio=convert_empty_strings_to_none(contract[-8]),
        price_min=convert_empty_strings_to_none(contract[-7]),
        price_avg=convert_empty_strings_to_none(contract[-6]),
        price_max=convert_empty_strings_to_none(contract[-5]),
        price_market=convert_empty_strings_to_none(contract[-4]),
        price_best_bid=convert_empty_strings_to_none(contract[-3]),
        price_best_call=convert_empty_strings_to_none(contract[-2]),
        num_of_lots=convert_empty_strings_to_none(contract[-1])
    )


def create_sections(all_values: list[str], sections: list[list[str]]) -> list[SectionSchema]:
    all_sections = []
    names_prefix = 'Секция Биржи: '
    names = get_searched_string_from_all_values(
        all_values, 
        search_value=names_prefix, 
        prefix=names_prefix)
    metrixes_prefix = 'Единица измерения: '
    metrixes = get_searched_string_from_all_values(
        all_values, 
        search_value=metrixes_prefix, 
        prefix=metrixes_prefix)
    
    section_index = 0
    for section in sections:
        all_sections.append(
            SectionSchema(
                name=names[section_index],
                metric=metrixes[section_index],
                contracts=get_contracts_from_section(section)
            )
        )
        section_index += 1
    return all_sections


def create_trade_day(all_values: list[str]) -> TradeDaySchema:
    sections_indexes = get_sections_indexes(all_values)
    sections = get_raw_sections(all_values, sections_indexes)
    return TradeDaySchema(
        day=fetch_day(all_values),
        sections=create_sections(all_values, sections)
    )


def fetch_trade_day(day: str) -> TradeDaySchema:
    converted_day = get_date(day)
    validated_day = validate_date(converted_day)
    url = get_url_to_spimex_data(validated_day)
    content = download_file_from_spimex(url)
    sheet = read_spimex_file(content)
    raw_data = get_all_cell_values_from_sheet(sheet)
    all_values = delete_all_emty_values_from_raw_data(raw_data)
    return create_trade_day(all_values)


def save_contract(contract: ContractSchema, section: Section) -> Contract:
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
        num_of_lots=contract.num_of_lots,
        section=section
    )


def save_trade_day_to_db(trade_day: TradeDaySchema) -> None:
    
    trade_day_db = TradeDay(day=trade_day.day)
    trade_day_db.save(force_insert=True)

    for section in trade_day.sections:
        section_db = Section(name=section.name, metric=section.metric, trade_day=trade_day_db)
        section_db.save(force_insert=True)
        for contract in section.contracts:
            contact_db = save_contract(contract=contract, section=section_db)
            contact_db.save(force_insert=True)
