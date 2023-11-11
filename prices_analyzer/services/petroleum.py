from collections import defaultdict

from prices_analyzer.shemas import Petroleum_sh, PetroleumConverter, Product_sh, ProductKey_sh
from prices_analyzer.models import Basis, Petroleum, ProductKey
from spimex_parser.shemas import Contract_sh, TradeDay_sh


def get_product_key(contract: Contract_sh) -> ProductKey_sh:
    return ProductKey_sh(
        name=contract.code[:4],
        base=contract.code[4:7],
        base_name=contract.base
    )


def get_contracts_volumes_sum(contracts: list[Contract_sh]) -> dict[ProductKey_sh, float]:
    products_volumes: dict[ProductKey_sh, float] = defaultdict(float)

    for contract in contracts:
        products_key = get_product_key(contract)

        products_volumes[products_key] += float(contract.volume)

    return products_volumes


def get_contracts_amount_sum(contracts: list[Contract_sh]) -> dict[ProductKey_sh, float]:
    products_amounts: dict[ProductKey_sh, float] = defaultdict(float)

    for contract in contracts:
        products_key = get_product_key(contract)

        products_amounts[products_key] += float(contract.amount)

    return products_amounts


def get_products_from_trade_day(trade_day: TradeDay_sh) -> list[Product_sh]:
    products: dict[ProductKey_sh, Product_sh] = {}
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


def save_product_key_base_to_db(petroleum: Petroleum_sh) -> tuple[ProductKey, bool]:
    obj, created = ProductKey.objects.get_or_create(
        code=petroleum.product_key.name,
        sort=petroleum.sort.value
        )
    return obj, created


def save_basis_to_db(product_key: ProductKey_sh) -> tuple[Basis, bool]:
    obj, created = Basis.objects.get_or_create(
        code=product_key.base,
        name=product_key.base_name
        )
    return obj, created


def save_petroleums_to_db(petroleums: list[Petroleum_sh]) -> None:
    for petroleum in petroleums:
        product_key = save_product_key_base_to_db(petroleum=petroleum)
        basis = save_basis_to_db(product_key=petroleum.product_key)
        
        Petroleum.objects.create(
            product_key=product_key[0],
            basis=basis[0],
            volume=petroleum.volume,
            price=petroleum.price,
            metric=petroleum.metric,
            day=petroleum.day,
            density=petroleum.density,
        )
