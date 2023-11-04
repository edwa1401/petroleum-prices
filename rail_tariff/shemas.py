# сделать загрузку base_from_name, base_from_code, base_from_rail_code

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True, slots=True)
class RailTariff:
    pass