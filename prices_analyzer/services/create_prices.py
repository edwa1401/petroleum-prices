import datetime
import decimal
import logging

from django.db.models.query import QuerySet

from prices_analyzer.models import Prices, ProductionPlace, Depot, Petroleum
from prices_analyzer.shemas import PetroleumSort
from rail_tariff.models import RailTariff
from django.db.models import Q


logger = logging.getLogger(__name__)

def get_period_for_petroleums(
        start_date: datetime.date,
        end_date: datetime.date) -> list[datetime.date]:

# TODO 1. разделить фнкцию на простые куски 2. Создать функцию, которая будет принимать depot
# и создавать prices для всех существующих petroleums
    
    delta = end_date - start_date
    
    return [start_date + datetime.timedelta(days=day) for day in range(delta.days + 1)]


def create_prices_for_all_depots_for_day(
        day: datetime.date) -> None:
    
    depots = Depot.objects.all().prefetch_related('rzd_code')
    
    production_places = ProductionPlace.objects.all(
    ).prefetch_related('rzd_code').prefetch_related('basis')

    production_places_bases = production_places.values_list('basis__code', flat=True)

    petroleums = Petroleum.objects.prefetch_related('basis').prefetch_related(
        'product_key').filter(
        Q(day=day)|
        Q(basis__code__in=production_places_bases)|
        Q(price__isnull=False)
        ).exclude(product_key__sort='Other products')

    
    rail_tariffs = RailTariff.objects.all().prefetch_related(
        'rail_code_base_to').prefetch_related('rail_code_base_from')
    
    for depot in depots:
        create_prices_for_depot(depot, production_places, petroleums, rail_tariffs)


def create_prices_for_depot(
        depot: Depot, 
        production_places: QuerySet[ProductionPlace],
        petroleums: QuerySet[Petroleum],
        rail_tariffs: QuerySet[RailTariff]
        ) -> None:
    
    logger.debug('depot=%s', depot)
    for production_place in production_places:
        create_prices_for_production_place(depot, production_place, petroleums, rail_tariffs)


def create_prices_for_production_place(
        depot: Depot, 
        production_place: ProductionPlace,
        petroleums: QuerySet[Petroleum],
        rail_tariffs: QuerySet[RailTariff],
        ) -> None:
    
    logger.debug('production place=%s', production_place)
    for petroleum in petroleums.filter(basis__code=production_place.basis.code):
        create_prices_for_petroleum(depot, production_place, petroleum, rail_tariffs)



AB = [PetroleumSort.AI100, PetroleumSort.AI98, PetroleumSort.AI95, PetroleumSort.AI92]
DT = [PetroleumSort.DTL, PetroleumSort.DTD, PetroleumSort.DTZ]


def get_cargo_code(petroleum_sort: PetroleumSort) -> int | None:

    if petroleum_sort in AB:
        return 21105
    elif petroleum_sort in DT:
        return 21404
    else:
        return None
    
    
def get_rail_tariff(
        depot: Depot,
        production_place: ProductionPlace,
        rail_tariffs: QuerySet[RailTariff],
        cargo: int | None) -> RailTariff | None:
    
    if not cargo:
        return None
    
    return rail_tariffs.filter(
        rail_code_base_to=depot.rzd_code,
        rail_code_base_from=production_place.rzd_code,
        cargo=cargo).first()


def save_prices_to_db(
                depot: Depot,
                production_place: ProductionPlace,
                petroleum: Petroleum,
                rail_tariff: RailTariff | None,
                full_price: decimal.Decimal | None
                ) -> bool:
    
    if not full_price:
        return False
    
    prices, create = Prices.objects.get_or_create(
        depot=depot,
        production_place=production_place,
        petroleum=petroleum,
        rail_tariff=rail_tariff,
        full_price=full_price
    )
    return create


def calculate_full_price(
        petroleum: Petroleum,
        rail_tarif: RailTariff | None
        ) -> decimal.Decimal | None:

    if not rail_tarif:
        return None

    if not petroleum.price:
        return None
    
    if petroleum.metric == 'Килограмм':
        return petroleum.price + (rail_tarif.tarif/1000)
    else:
        return petroleum.price + rail_tarif.tarif
    

def create_prices_for_petroleum(
        depot: Depot, 
        production_place: ProductionPlace,
        petroleum: Petroleum,
        rail_tariffs: QuerySet[RailTariff]
        ) -> None:
    
    logger.debug('petroleum=%s', petroleum)
    cargo = get_cargo_code(PetroleumSort[petroleum.product_key.sort])
    rail_tariff = get_rail_tariff(depot, production_place, rail_tariffs, cargo)
    full_price = calculate_full_price(petroleum, rail_tariff)
    prices = save_prices_to_db(
        depot=depot,
        production_place=production_place,
        petroleum=petroleum,
        rail_tariff=rail_tariff,
        full_price=full_price
    )
    logger.debug('prices=%s', prices)



# def create_prices_for_all_depots_for_day(
#         day: datetime.date) -> None:
    
#     depots = Depot.objects.all().prefetch_related('rzd_code')
    
#     production_places = ProductionPlace.objects.all(
#     ).prefetch_related('rzd_code').prefetch_related('basis')

#     production_places_bases = production_places.values_list('basis__code', flat=True)

#     petroleums = Petroleum.objects.prefetch_related('basis').prefetch_related(
#         'product_key').filter(
#         Q(day=day)|
#         Q(basis__code__in=production_places_bases)|
#         Q(price__isnull=False)
#         ).exclude(product_key__sort='Other products')

    
#     rail_tariffs = RailTariff.objects.all().prefetch_related(
#         'rail_code_base_to').prefetch_related('rail_code_base_from')
    
#     for depot in depots:
#         for production_place in production_places:
#             for petroleum in petroleums.filter(basis__code=production_place.basis.code):
#                 cargo = get_cargo_code(PetroleumSort[petroleum.product_key.sort])
#                 if cargo:
#                     rail_tariff = rail_tariffs.filter(
#                         rail_code_base_to=depot.rzd_code,
#                         rail_code_base_from=production_place.rzd_code,
#                         cargo=cargo).first()

#                     if rail_tariff:
#                         full_price = calculate_full_price(petroleum, rail_tariff)
#                         if full_price:
#                             prices = save_prices_to_db(
#                                 depot=depot,
#                                 production_place=production_place,
#                                 petroleum=petroleum,
#                                 rail_tariff=rail_tariff,
#                                 full_price=full_price
#                             )
#                             logger.info('prices=%s', prices)
    




