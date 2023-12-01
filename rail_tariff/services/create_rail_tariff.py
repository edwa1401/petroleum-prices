from django.shortcuts import get_object_or_404
from prices_analyzer.models import Depot, ProductionPlace
from rail_tariff.models import RailTariff, RzdCode
from rail_tariff.shemas import Fuel, RailTariffClient
from rail_tariff import shemas
import time


def get_rail_tariff_from_spimex(
        station_to: str,
        station_from: str,
        cargo: str,
        ves: str
        ) -> shemas.RailTariff:

    rail_tarif = RailTariffClient()

    return rail_tarif.get_rail_tariff(station_to=station_to,
            station_from=station_from,
            cargo=cargo,
            ves=ves)


def save_rail_tariff_to_db(
        station_to: str,
        station_from: str,
        cargo: str,
        ves: str,
        tariff: shemas.RailTariff) -> bool:

    try:
        rail_code_base_to = get_object_or_404(RzdCode, code=station_to)
        rail_code_base_from = get_object_or_404(RzdCode, code=station_from)

        rail_data, create = RailTariff.objects.get_or_create(
            rail_code_base_to=rail_code_base_to,
            rail_code_base_from=rail_code_base_from,
            weight=ves,
            cargo=cargo,
            distance=tariff.distance,
            tarif=tariff.tarif
        )
    except (TypeError, ValueError) as e:
        f'incorrect data format {e}'
    return create


def get_prod_places_codes() -> list[str]:
    prod_places = ProductionPlace.objects.all().select_related('rzd_code')
    prod_places_codes = []
    for prod_place in prod_places:
        if str(prod_place.rzd_code.code) not in prod_places_codes and \
        str(prod_place.rzd_code.code) != '0':
            prod_places_codes.append(str(prod_place.rzd_code.code))
            
    return prod_places_codes

class IncorrectCargoValueError(Exception):
    pass


def get_rail_tariffs_for_depot(depot_id: int, fuel: Fuel) -> None:
    production_places_codes = get_prod_places_codes()
    depot = get_object_or_404(Depot, id=depot_id)
    station_to = str(depot.rzd_code.code)
    if fuel.value == 'AB':
        cargo = '21105'
        ves = '52'
    elif fuel.value == 'DT':
        cargo = '21404'
        ves = '55'
    
    else:
        raise IncorrectCargoValueError

    for station_from in production_places_codes:
        tariff = get_rail_tariff_from_spimex(
            station_to=station_to,
            station_from=station_from,
            cargo=cargo,
            ves=ves,
        )

        time.sleep(1)
        save_rail_tariff_to_db(station_to, station_from, cargo, ves, tariff)
