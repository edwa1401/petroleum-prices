from rail_tariff.services import create_rail_tariff
from rail_tariff import schemas


def test__get_cargo_ves_for_fuel__success():
    fuel = schemas.Fuel['AB']

    expected = ('21105', '52')

    assert create_rail_tariff.get_cargo_ves_for_fuel(fuel) == expected
