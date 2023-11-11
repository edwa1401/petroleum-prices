import csv

from prices_analyzer.models import Basis, ProductionPlace

def create_prod_place_map() -> dict[str, list[str]]:
    prod_place_map = {}
    with open ('data/basis_prod_map.csv', 'r', encoding='utf8-') as f:
        csv_reader = csv.reader(f, delimiter = ';')
        next(csv_reader)
        for row in csv_reader:
            prod_place_map[row[0]] = [row[1], row[2]]
    return prod_place_map


def create_prod_places() -> None:
    prod_places = create_prod_place_map()
    for prod_place in prod_places:
        basis, create = Basis.objects.get_or_create(code=prod_place, name='')
        prod_place, create = ProductionPlace.objects.get_or_create(
            basis=basis,
            rzd_code=prod_places[prod_place][0],
            name=prod_places[prod_place][1]
            )
