import datetime
import decimal
import logging

from prices_analyzer.models import Prices, ProductionPlace, Depot, Petroleum
from prices_analyzer.shemas import PetroleumSort
from rail_tariff.models import RailTariff
from django.db.models import Q


logger = logging.getLogger(__name__)

def get_period_for_petroleums(
        start_date: datetime.date,
        end_date: datetime.date) -> list[datetime.date]:
    
    delta = end_date - start_date
    
    return [start_date + datetime.timedelta(days=day) for day in range(delta.days + 1)]


def create_prices_for_all_depots_for_day(
        day: datetime.date) -> None:
    
    depots = Depot.objects.all().prefetch_related('rzd_code')

    logger.info('depots=%s', depots)
    
    production_places = ProductionPlace.objects.all(
    ).prefetch_related('rzd_code').prefetch_related('basis')

    logger.info('production places=%s', production_places)

    production_places_bases = production_places.values_list('basis__code', flat=True)

    petroleums = Petroleum.objects.prefetch_related('basis').prefetch_related(
        'product_key').filter(
        Q(day=day)|
        Q(basis__in=production_places_bases)|
        Q(price__isnull=False)
        ).exclude(product_key__sort='Other products')
    
    logger.info('petroleums=%s', petroleums)
    
    rail_tariffs = RailTariff.objects.all().prefetch_related(
        'rail_code_base_to').prefetch_related('rail_code_base_from')
    
    logger.info('rail_tariffs=%s', rail_tariffs)

    for depot in depots:
        for production_place in production_places:
            for petroleum in petroleums.filter(basis=production_place.basis):

                cargo = get_cargo_code(PetroleumSort[petroleum.product_key.sort])
                if cargo:
                    rail_tariff = rail_tariffs.filter(
                        rail_code_base_to=depot.rzd_code,
                        rail_code_base_from=production_place.rzd_code,
                        cargo=cargo).first()

                    if rail_tariff:
                        full_price = calculate_full_price(petroleum, rail_tariff)
                        if full_price:
                            save_prices_to_db(
                                depot=depot,
                                production_place=production_place,
                                petroleum=petroleum,
                                rail_tariff=rail_tariff,
                                full_price=full_price
                            )


AB = [PetroleumSort.AI100, PetroleumSort.AI98, PetroleumSort.AI95, PetroleumSort.AI92]
DT = [PetroleumSort.DTL, PetroleumSort.DTD, PetroleumSort.DTZ]

def get_cargo_code(petroleum_sort: PetroleumSort) -> int | None:

    if petroleum_sort in AB:
        return 21105
    elif petroleum_sort in DT:
        return 21404
    else:
        return None


def save_prices_to_db(
                depot: Depot,
                production_place: ProductionPlace,
                petroleum: Petroleum,
                rail_tariff: RailTariff,
                full_price: decimal.Decimal
                ) -> bool:
    
    prices, create = Prices.objects.get_or_create(
        depot=depot,
        production_place=production_place,
        petroleum=petroleum,
        rail_tariff=rail_tariff,
        full_price=full_price
    )
    return create


def calculate_full_price(petroleum: Petroleum, rail_tarif: RailTariff) -> decimal.Decimal | None:

    if petroleum.price:
        if petroleum.metric == 'Метрическая тонна':
            return petroleum.price + rail_tarif.tarif
        else:
            return petroleum.price + (rail_tarif.tarif/1000)
    else:
        return None
