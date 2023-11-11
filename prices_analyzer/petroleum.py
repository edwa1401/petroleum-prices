from collections import defaultdict

from prices_analyzer.shemas import Petroleum_sh, PetroleumConverter, Product_sh, ProductKey
from prices_analyzer.models import Petroleum
from spimex_parser.shemas import Contract_sh, TradeDay_sh


def get_product_key(contract: Contract_sh) -> ProductKey:
    return ProductKey(
        name=contract.code[:4],
        base=contract.code[4:7],
        base_name=contract.base
    )


def get_contracts_volumes_sum(contracts: list[Contract_sh]) -> dict[ProductKey, float]:
    products_volumes: dict[ProductKey, float] = defaultdict(float)

    for contract in contracts:
        products_key = get_product_key(contract)

        products_volumes[products_key] += float(contract.volume)

    return products_volumes


def get_contracts_amount_sum(contracts: list[Contract_sh]) -> dict[ProductKey, float]:
    products_amounts: dict[ProductKey, float] = defaultdict(float)

    for contract in contracts:
        products_key = get_product_key(contract)

        products_amounts[products_key] += float(contract.amount)

    return products_amounts


def get_products_from_trade_day(trade_day: TradeDay_sh) -> list[Product_sh]:
    products: dict[ProductKey, Product_sh] = {}
    for section in trade_day.sections:
        amounts = get_contracts_amount_sum(section.contracts)
        volumes = get_contracts_volumes_sum(section.contracts)
        for contract in section.contracts:
            product_key = get_product_key(contract)
            if product_key in products:
                continue

            product = Product_sh(
                product_key=product_key,
                volume=volumes[product_key],
                amount=amounts[product_key],
                day=trade_day.day,
                metric=section.metric
            )
            products[product_key] = product
    return list(products.values())


def get_petroleums_from_products(products: list[Product_sh]) -> list[Petroleum_sh]:
    converter = PetroleumConverter()
    converter.load()
    return [converter.convert(product) for product in products]


def save_petroleums_to_db(petroleums: list[Petroleum_sh]) -> None:
    for petroleum in petroleums:
        Petroleum.objects.create(
            product_key=petroleum.product_key.name,
            base=petroleum.product_key.base,
            base_name=petroleum.product_key.base_name,
            volume=petroleum.volume,
            amount=petroleum.amount,
            metric=petroleum.metric,
            day=petroleum.day,
            sort=petroleum.sort.value,
            density=petroleum.density,
            price=petroleum.price,
            retail_price=petroleum.retail_price
        )

