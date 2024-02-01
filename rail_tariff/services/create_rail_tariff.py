import logging
import backoff
from django.shortcuts import get_object_or_404
import requests
from prices_analyzer.models import Depot, ProductionPlace
from rail_tariff.models import RailTariff, RzdStation
from rail_tariff.shemas import Fuel, RailTariffClient
from rail_tariff import shemas
import time
import random

logger = logging.getLogger(__name__)


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
        rail_code_base_to = get_object_or_404(RzdStation, code=station_to)
        rail_code_base_from = get_object_or_404(RzdStation, code=station_from)

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
        if prod_place.rzd_code.code not in prod_places_codes and \
        prod_place.rzd_code.code != '0':
            prod_places_codes.append(prod_place.rzd_code.code)

    return prod_places_codes


class IncorrectCargoValueError(Exception):
    pass


def get_cargo_ves_for_fuel(fuel: Fuel) -> tuple[str, str]:
    
    if fuel.value == 'AB':
        cargo = '21105'
        ves = '52'
    elif fuel.value == 'DT':
        cargo = '21404'
        ves = '55'
    
    else:
        raise IncorrectCargoValueError
    
    return cargo, ves



def check_rail_tarif_exists(station_to: str, station_from: str, cargo: str) -> bool:

    rail_code_base_to = get_object_or_404(RzdStation, code=station_to)
    rail_code_base_from = get_object_or_404(RzdStation, code=station_from)

    rail_tariffs = RailTariff.objects.filter(
        rail_code_base_to=rail_code_base_to,
        rail_code_base_from=rail_code_base_from,
        cargo=int(cargo)
        )
    
    if not rail_tariffs:
        return False
    
    return True

def get_tarif_from_spimex(
        station_to: str,
        station_from: str,
        cargo: str,
        ves: str) -> shemas.RailTariff:
    
    
    rail_tarif_client = RailTariffClient()

    logger.info(
        'req works: to=%s, from=%s, cargo=%s', station_to, station_from, cargo
        )
    tariff = rail_tarif_client.get_rail_tariff(
        station_to=station_to,
        station_from=station_from,
        cargo=cargo,
        ves=ves,
        )
    
    
    return tariff


@backoff.on_exception(
        backoff.constant,
        requests.exceptions.ConnectTimeout,
        jitter=None,
        max_tries=10,
        interval=60)

def get_rail_tariffs_for_depot(depot_id: int) -> None:
    
    production_places_codes = get_prod_places_codes()
    depot = get_object_or_404(Depot, id=depot_id)
    station_to = str(depot.rzd_code.code)

    fuels = [Fuel['AB'], Fuel['DT']]

    for station_from in production_places_codes:
        for fuel in fuels:
            cargo, ves = get_cargo_ves_for_fuel(fuel)
            if not check_rail_tarif_exists(station_to, station_from, cargo):

                tariff = get_tarif_from_spimex(station_to, station_from, cargo, ves)

                save_rail_tariff_to_db(station_to, station_from, cargo, ves, tariff)

                sleep = random.random()*5 + 0.1

                time.sleep(sleep)


def get_tariffs_for_all_depots() -> None:
    depots_id = Depot.objects.all().values_list('pk', flat=True)
    for depot_id in depots_id:
        get_rail_tariffs_for_depot(int(depot_id))

