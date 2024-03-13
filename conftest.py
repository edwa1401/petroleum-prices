import datetime
import io
import random
import string
from unittest.mock import patch

import pytest
import requests
from faker import Faker
from prices_analyzer.models import Depot

from prices_analyzer.schemas import ProductKeySchema, ProductSchema
from rail_tariff.models import RzdStation
from spimex_parser.models import TradeDay
from spimex_parser.schemas import ContractSchema, SectionSchema, TradeDaySchema
from users.models import User

pytest_plugins = ("celery.contrib.pytest", )

@pytest.fixture
def contract_volume():
    return round(random.uniform(1.00, 100000000.99), 2)


@pytest.fixture
def contract_amount():
    return round(random.uniform(1.00, 100000000000000.99), 2)
    

@pytest.fixture
def make_random_string():
    def inner(
        num_letters: int | None = None,
        num_digits: int | None = None,
    ):
        letters = ''.join(random.choices(string.ascii_uppercase, k=num_letters or 0))
        digits = ''.join(random.choices(string.digits, k=num_digits or 0))
        return letters + digits
    return inner


@pytest.fixture
def make_trade_code():
    def inner(
            product: str | None = None,
            basis: str | None = None,
            lot_size: str | None = None,
            shipment: str | None = None
    ):
        product = product or ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        basis = basis or ''.join(random.choices(string.ascii_uppercase, k=3))
        lot_size = lot_size or ''.join(random.choices(string.digits, k=3))
        shipment = shipment or random.choice(string.ascii_uppercase)
        return product + basis + lot_size + shipment
    return inner


@pytest.fixture
def contract_petroleum_price():
    return str(round(random.uniform(1.00, 1000000.99), 2))


@pytest.fixture
def make_xls_contract_row(make_trade_code, contract_petroleum_price, contract_volume, contract_amount):
    def inner(
            code: str | None = None,
            name: str | None = None,
            base: str | None = None,
            volume: str | None = None,
            amount: str | None = None,
            price_change_amount: str | None = None,
            price_change_ration: str | None = None,
            price_min: str | None = None,
            price_avg: str | None = None,
            price_max: str | None = None,
            price_market: str | None = None,
            price_best_bid: str | None = None,
            price_best_call: str | None = None,
            num_of_lot: str | None = None
    ):
        code = code or make_trade_code
        name = name or 'Продукт (марка бензина/сорт ДТ), ст. отправления'
        base = base or 'жд станция / пункт налива / нефтебаза'
        volume = volume or str(contract_volume)
        amount = amount or str(contract_amount)
        price_change_amount = price_change_amount or str(random.randint(60, 1000))
        price_change_ration = price_change_ration or str(round(random.uniform(0.1, 100.0), 2))
        price_min = price_min or contract_petroleum_price
        price_avg = price_avg or contract_petroleum_price
        price_max = price_max or contract_petroleum_price
        price_market = price_market or contract_petroleum_price
        price_best_bid = price_best_bid or contract_petroleum_price
        price_best_call = price_best_call or contract_petroleum_price
        num_of_lot = num_of_lot or str(random.randint(0, 50))
        return [
            code, name, base, volume, amount, price_change_amount,
            price_change_ration, price_min, price_avg, price_max,
            price_market, price_best_bid, price_best_call, num_of_lot
        ]
    return inner


@pytest.fixture
def create_contracts_str(make_xls_contract_row):
    def inner(num_of_contracts: int | None = None):
        num_of_contracts = num_of_contracts or 10
        return [make_xls_contract_row for _ in range(num_of_contracts)]
    return inner


@pytest.fixture
def make_section_str(create_contracts_str):
    def inner(
            name: str | None = None,
            metrix: str | None = None,
            contracts: list[list[str]] | None = None
    ):
        name = name or 'Нефтепродукты» АО «СПбМТСБ'
        metrix = metrix or random.choice(['Килограмм','Метрическая тонна'])
        contracts = contracts or create_contracts_str
        return [name, metrix, contracts]
    return inner


@pytest.fixture
def create_sections_str(make_section_str):
    def inner(num_of_sections: int | None = None):
        num_of_sections = num_of_sections or 2
        return [make_section_str for _ in range(num_of_sections)]
    return inner


@pytest.fixture
def make_trade_day_str(create_sections_str, make_date_str):
    def inner(day: str | None = None,
              sections: list[list[list[str]]] | None = None
              ):
        day = day or make_date_str
        sections = sections or create_sections_str
        return [day, sections]
    return inner


@pytest.fixture
def create_all_values(create_contracts_str, make_date_str):
    def inner(
            first_row: str | None = None,
            prefix_day: str | None = None,
            section_name_str: str | None = None,
            metric_str: str | None = None,
            last_column_header: str | None = None,
            total_line_contracts: str | None = None
    ):
        first_row = first_row or 'Бюллетень'
        prefix_day = prefix_day or 'Дата торгов: '
        day = make_date_str
        section_name_str = section_name_str or 'Секция Биржи: «Нефтепродукты» АО «СПбМТСБ»'
        metric_str = metric_str or 'Единица измерения: Метрическая тонна'
        last_column_header = 'Лучший\nспрос'
        total_line_contracts = 'Итого:'
        contracts = create_contracts_str
        all_values = [
            first_row,
            prefix_day,
            day,
            section_name_str,
            metric_str,
            last_column_header,
            ''.join([contract for contract in contracts]),
            total_line_contracts,
            last_column_header,
            ''.join([contract for contract in contracts]),
            total_line_contracts
        ]
        return all_values
    return inner


@pytest.fixture
def convert_bytes_from_str():
    def inner(value: str | None):
        value = value or 'anything'
        return value.encode()
    return inner


@pytest.fixture
def make_request_response(convert_bytes_from_str):
    def inner(
            value: str | None = None
    ):
        response = requests.Response()
        response.status_code = 200
        response.raw = io.BytesIO(convert_bytes_from_str(value=value))
        return response
    return inner


@pytest.fixture
def make_date_str():
    def inner(day: str | None = None):
        fake = Faker()
        day = day or datetime.datetime.strftime(fake.date_object(), '%d.%m.%Y')
        return day
    return inner


@pytest.fixture
def make_date(make_date_str):
    def inner(day: str | None = None):
        day = day or make_date_str
        return datetime.datetime.strptime(day, '%d.%m.%Y')
    return inner


@pytest.fixture
def create_day():
    def inner(day: str | None = None):
        fake = Faker()
        day = day or fake.date()
        return datetime.date.fromisoformat(day)
    return inner
    


@pytest.fixture
def create_contract(make_xls_contract_row):
    def inner(
            code: str | None = None,
            name: str | None = None,
            base: str | None = None,
            volume: str | None = None,
            amount: str | None = None,
            price_change_amount: str | None = None,
            price_change_ratio: str | None = None,
            price_min: str | None = None,
            price_avg: str | None = None,
            price_max: str | None = None,
            price_market: str | None = None,
            price_best_bid: str | None = None,
            price_best_call: str | None = None,
            num_of_lots: str | None = None
    ):
        contract = make_xls_contract_row()
        return ContractSchema(
            code=code or contract[0],
            name=name or contract[1],
            base=base or contract[2],
            volume=volume or contract[3],
            amount=amount or contract[4],
            price_change_amount=price_change_amount or contract[5],
            price_change_ratio=price_change_ratio or contract[6],
            price_min=price_min or contract[7],
            price_avg=price_avg or contract[8],
            price_max=price_max or contract[9],
            price_market=price_market or contract[10],
            price_best_bid=price_best_bid or contract[11],
            price_best_call=price_best_call or contract[12],
            num_of_lots=num_of_lots or contract[13]
        )
    return inner

@pytest.fixture
def create_product_key(make_trade_code, create_contract):
    def inner(code: str | None = None,
              base_name: str | None = None):

        code = code or make_trade_code
        base_name = base_name or 'жд станция'

        contract = create_contract(code=code, base=base_name)

        return ProductKeySchema(
            name=contract.code[0:4],
            base=contract.code[4:7],
            base_name=contract.base
        )
    return inner

@pytest.fixture
def create_trade_day(create_contract, make_date, make_trade_code, contract_volume, contract_amount):
    def inner(input_day: str | None = None,
              section_names: list[str] | None = None,
              section_metrics: list[str] | None = None,
              contracts: list[list[ContractSchema], list[ContractSchema]] | None = None,
              ):
        day = make_date(input_day) or make_date
        base = 'жд станция'

        section_names = section_names or ['«Нефтепродукты» АО «СПбМТСБ»', '«Нефтепродукты» АО «СПбМТСБ»']
        section_metrics = section_metrics or ['Килограмм', 'Метрическая тонна']

        contracts = contracts or [
            [create_contract(code=make_trade_code, base=base, volume=contract_volume, amount=contract_amount) for _ in range(random.randint(0, 10))],
            [create_contract(code=make_trade_code, base=base, volume=contract_volume, amount=contract_amount) for _ in range(random.randint(0, 10))]
        ]
        return TradeDaySchema(
            day=day,
            sections=[
                SectionSchema(
                    name=section_names[0],
                    metric=section_metrics[0],
                    contracts=contracts[0]
                ),
                SectionSchema(
                    name=section_names[1],
                    metric=section_metrics[1],
                    contracts=contracts[1]
                ),
            ]
        )
    return inner


@pytest.fixture
def create_product(create_product_key, make_date, contract_volume, contract_amount):
    def inner(
            product_key: ProductKeySchema | None = None,
            volume: float | None = None,
            amount: float | None = None,
            metric: str | None = None,
            inp_day: str | None = None
    ):
        product_key = product_key or create_product_key
        volume = volume or contract_volume
        amount = amount or contract_amount
        metric = metric or random.choice(['Килограмм','Метрическая тонна'])
        day = make_date(inp_day) or make_date

        return ProductSchema(
            product_key=product_key,
            volume=volume,
            amount=amount,
            metric=metric,
            day=day
        )
    return inner


@pytest.fixture
def xlrd_open_workbook_mock():
    with patch('xlrd.open_workbook') as mock:
        yield mock


@pytest.fixture
def download_file_mock():
    with patch('spimex_parser.parser.download_file') as mock:
        yield mock


@pytest.mark.django_db
@pytest.fixture
def create_rzd_station() -> RzdStation:
    def inner(
            code: str | None = None,
            station_name: str | None = None):
        code = code or '12345'
        station_name = station_name or 'Station'
        return RzdStation.objects.create(code=code, station_name=station_name)
    return inner


@pytest.mark.django_db
@pytest.fixture
def create_trade_day_db(create_day) -> TradeDay:
    def inner(
            day: str | None = None):
        day = day or create_day
        return TradeDay.objects.create(day=day)
    return inner


@pytest.fixture
def create_signal_for_created_depot_mock():
    with patch('prices_analyzer.signals.get_rail_tariffs_for_created_depot') as mock:
        yield mock


@pytest.mark.django_db
@pytest.fixture
def create_depot_db(
    client,
    django_user_model,
    create_rzd_station,
    make_random_string,
    ) -> Depot:
    def inner(
            name: str | None = None,
            user: User | None = None,
            rzd_code: RzdStation | None = None):
        username = 'user'
        password = 'password'
        name = name or make_random_string
        rzd_code = rzd_code or create_rzd_station()
        user = django_user_model.objects.create_user(username=username, password=password)
        client.force_login(user)
        return Depot.objects.create(name=name, user=user, rzd_code=rzd_code)
    return inner



