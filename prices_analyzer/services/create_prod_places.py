import csv
import logging

from prices_analyzer.models import Basis, ProductionPlace
from rail_tariff.models import RzdStation

logger = logging.getLogger(__name__)

def create_prod_place_map() -> dict[str, list[str]]:
    prod_place_map = {}
    with open ('data/basis_prod_map.csv', 'r', encoding='utf8-') as f:
        csv_reader = csv.reader(f, delimiter = ';')
        next(csv_reader)
        for row in csv_reader:
            prod_place_map[row[0]] = [row[1], row[2], row[3]]
    return prod_place_map


def update_prod_places() -> None:
    prod_places = create_prod_place_map()

    for prod_place in prod_places:
        logger.debug('prod_place=%s', prod_place)
        basis, create = Basis.objects.get_or_create(code=prod_place)
        logger.debug('basis=%s', basis)
        rzd_code, created = RzdStation.objects.update_or_create(
            defaults={'station_name': prod_places[prod_place][2]},
            code=prod_places[prod_place][0],
            )
        prod_place, create = ProductionPlace.objects.get_or_create(
            basis=basis,
            rzd_code=rzd_code,
            name=prod_places[prod_place][1],
            )

