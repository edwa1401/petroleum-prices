
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
        'day': prices.petroleum.day,
        'depot': prices.depot.name,
        'production_place': prices.production_place.name,
        'sort': prices.petroleum.product_key.sort,
        'metric': prices.petroleum.metric,
        'volume': prices.petroleum.volume,
        'price_at_prodiction_place': prices.petroleum.price,
        'rail_tariff': prices.rail_tariff.tarif,
        'price_at_depot': prices.full_price,
        'distance_from_production_to_depot': prices.rail_tariff.distance
        }  
