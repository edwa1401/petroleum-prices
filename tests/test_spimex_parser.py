import datetime
from django.test import TestCase
from spimex_parser import parser
import pytest
from unittest.mock import patch


@pytest.mark.parametrize(
        ('date, expected'),
        [('2023-02-11', datetime.date(2023, 2, 11)),
         ('2021-10-02', datetime.date(2021, 10, 2))
         ]
)
def test__get_date__success(date, expected):
    assert parser.get_date(date) == expected


@pytest.mark.parametrize(
        ('data, expected'),
        [
            (datetime.date(2023, 11, 8), '20231108'),
            (datetime.date(2023, 1, 18), '20230118'),
            (datetime.date(2023, 9, 1), '20230901'),

        ],
        ids=[
            "add zero to one simbol's day",
            "add zero to one simbol's month",
            'add zeros to month and day'
        ]
)
def test__convert_date__success(data, expected):
    assert parser.convert_date(data) == expected


@pytest.mark.parametrize(
        ('data'),
        [
            (datetime.date(2023, 11, 4)),
            (datetime.date(2023, 10, 28)),
        ]
)

def test__validate_date__fail_for_weekend_days(data):
    assert parser.convert_date(data) is None


def test__convert_empty_strings__success_return_none_for_value_is_dash():
    assert parser.convert_empty_strings_to_none('-') is None


def test__convert_empty_strings__return_string_when_value_is_not_dash():
    assert parser.convert_empty_strings_to_none('abc') == 'abc'


@pytest.mark.parametrize(
    ('date, expected'),
    [
        ('20230707', 'https://spimex.com/upload/reports/oil_xls/oil_xls_20230707162000.xls'),
        ('20230705', 'https://spimex.com/upload/reports/oil_xls/oil_xls_20230705162000.xls')
    ],

)
def test__get_url_to_spimex_data__success(date, expected):
    assert parser.get_url_to_spimex_data(date) == expected

@pytest.mark.parametrize(
    ('date, expected'),
    [
        ('20230707', 'https://spimex.com/upload/reports/oil_xls/oil_xls_20230708162000.xls'),
        ('20230705', 'https://spimex.com/upload/reports/oil_xls/oil_xls_20230705262000.xls'),
    ],
    ids=
    [
        "differen data",
        "misstake in uls ending"
    ]
)
def test__get_url_to_spimex_data__fail(date, expected):
    with pytest.raises(AssertionError):
        assert parser.get_url_to_spimex_data(date) == expected


def test__download_file__success(make_request_response):
    value = 'some value'
    with patch('spimex_parser.parser.requests.get') as requests_get_mock:
        requests_get_mock.return_value = make_request_response(value)
        assert parser.download_file('some_url') == b'some value'


@pytest.mark.parametrize(('raw_data, expected'),
                         [
                             (['', 'first_word', '', 'second_word', ''], ['first_word', 'second_word']),
                             (['one', 'two'], ['one', 'two'])
]
)
def test__delete_all_emty_values_from_raw_data__success(raw_data, expected):
    assert parser.delete_all_emty_values_from_raw_data(raw_data) == expected


@pytest.mark.parametrize(('all_values, search_value, expected'),
                         [
                             (['one', 'two', 'tree', 'four', 'tree'], 'tree', [2, 4]),
                             (['1', '2', '3', '4', '5'], '6', [])
])
def test__get_indexes_for_search_value__success(all_values, search_value, expected):
    assert parser.get_indexes_for_search_value(all_values, search_value) == expected


@pytest.mark.parametrize(('raw_string, prefix, expected'),
                         [
                             ('prepword', 'prep', 'word'),
                             ('somesimbol', 'other', 'somesimbol')
])
def test__extract_value_from_string__succes(raw_string, prefix, expected):
    assert parser.extract_value_from_string(raw_string, prefix) == expected


@pytest.mark.parametrize(('all_values, search_value, prefix, expected'),
                         [
                             (['prepone', 'two', 'tree', 'preptwo', 'tree'], 'prep', 'prep', ['one', 'two']),
                             (['1', '2', '3', '4', '5'], '6', '6', [])
])
def test__get_searched_string_from_all_values__success(all_values, search_value, prefix, expected):
    assert parser.get_searched_string_from_all_values(all_values, search_value, prefix) == expected


def test__convert_contract__success(make_contract_str, make_code, make_petroleum_price, create_contract):

    code = make_code(product='A100', basis='UFM', lot_size='060', shipment='F')
    price = make_petroleum_price
    name = 'Продукт (марка бензина/сорт ДТ), ст. отправления'
    base = 'жд станция / пункт налива / нефтебаза'
    volume = '120'
    amount = '2400000'
    price_change_amount = '1000'
    price_change_ration = '0.50'
    num_of_lot = '1'

    contract = make_contract_str(
        code=code,
        name=name,
        base=base,
        volume=volume,
        amount=amount,
        price_change_amount=price_change_amount,
        price_change_ration=price_change_ration,
        price_min=price,
        price_avg=price,
        price_max=price,
        price_market=price,
        price_best_bid=price,
        price_best_call=price,
        num_of_lot=num_of_lot
    )

    expected = create_contract(
        code=code,
        name=name,
        base=base,
        volume=volume,
        amount=amount,
        price_change_amount=price_change_amount,
        price_change_ratio=price_change_ration,
        price_min=price,
        price_avg=price,
        price_max=price,
        price_market=price,
        price_best_bid=price,
        price_best_call=price,
        num_of_lots=num_of_lot
    )

    assert parser.convert_contract(contract=contract) == expected


def test__convert_contract__fail_return_assertion_error_for_different_result_in_code(
        make_contract_str,
        make_code,
        create_contract):

    code = make_code(product='A100', basis='UFM', lot_size='060', shipment='F')

    contract = make_contract_str(code=code)

    expected = create_contract(code='A595UFM060F')

    with pytest.raises(AssertionError):
        assert parser.convert_contract(contract=contract) == expected


def test__get_spimex_sheet_for_day__open_first_sheet_from_excel(
        xlrd_open_workbook_mock, download_file_mock
        ):
    download_file_mock
    parser.get_spimex_sheet_for_day(datetime.datetime(2023, 12, 8))
    xlrd_open_workbook_mock.return_value.sheet_by_index.assert_called_once_with(0)


@pytest.mark.parametrize(
        ('data'),
        [
            (datetime.datetime(2023, 12, 17)),
            (datetime.datetime(2023, 12, 16)),
            (datetime.datetime(2023, 12, 9))
        ]
)
def test__get_spimex_sheet_for_day__fail_at_weekends(data):

    with pytest.raises(parser.NoTradingAtWeekendsExeption):
        assert parser.get_spimex_sheet_for_day(day=data)

