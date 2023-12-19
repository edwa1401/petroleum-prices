
from prices_analyzer.models import Petroleum, Prices
from typing import Any


def serialize_petroleum(petroleum: Petroleum) -> dict[str, Any]:
    return {
        'day': petroleum.day,
        'sort': petroleum.product_key.sort,
        'basis': petroleum.basis.name,
        'volume': petroleum.volume,
        'price': petroleum.price,
        'metric': petroleum.metric,
    }   

def serialize_prices(prices: Prices) -> dict[str, Any]:
    return {
        'depot': prices.depot.name,
        'production place': prices.production_place.name,
        'sort': prices.petroleum.product_key.sort,
        'metric': prices.petroleum.metric,
        'volume': prices.petroleum.volume,
        'price at prodiction place': prices.petroleum.price,
        'rail tariff': prices.rail_tariff.tarif,
        'price at depot': prices.full_price,
        'distance from production to depot': prices.rail_tariff.distance
        }  
