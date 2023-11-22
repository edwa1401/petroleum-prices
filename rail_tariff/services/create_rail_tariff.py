from rail_tariff.models import RailTariff
from rail_tariff.shemas import RailTariffSchema, RailTariffGetter


def get_rail_tariff_from_spimex(
        station_to: str,
        station_from: str,
        cargo: str,
        ves: str
        ) -> RailTariffSchema:


    rail_tarif = RailTariffGetter(
            station_to=station_to,
            station_from=station_from,
            cargo=cargo,
            ves=ves
        )
    return rail_tarif.get_rail_tariff()



def save_rail_tariff_to_db(rail_tariff: RailTariffSchema) -> None:

    try:
        # TODO get rail_code_base_to from Depot
        # get rail_code_base_from from Production Place

        rail_data, create = RailTariff.objects.get_or_create(
            rail_code_base_to=rail_tariff.rail_code_base_to,
            rail_code_base_from=rail_tariff.rail_code_base_from,
            weight=rail_tariff.weight,
            distance=rail_tariff.distance,
            tarif=rail_tariff.tarif
        )
    except (TypeError, ValueError) as e:
        f'incorrect data format {e}'
