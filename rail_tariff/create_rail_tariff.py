from rail_tariff.shemas import RailTariff_sh, RailTariffGetter


def get_rail_tariff_from_spimex(
        station_to: str,
        station_from: str,
        cargo: str,
        ves: str
        ) -> RailTariff_sh:


    rail_tarif = RailTariffGetter(
            station_to=station_to,
            station_from=station_from,
            cargo=cargo,
            ves=ves
        )
    return rail_tarif.get_rail_tariff()