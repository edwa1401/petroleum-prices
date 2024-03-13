import decimal
import enum
from dataclasses import dataclass

from pydantic import BaseModel, Field


SPIMEX_RZD_CARGO_TYPE = '43'
SPIMEX_RZD_CARGO_TONNAGE = '66'
NUMBER_OF_VAGONS = '1'
NUMBER_OF_SECURED_VAGONS = '1'
NUMBER_OF_CONDUCTORS = '0'
NUMBER_OF_AXLES = '4'
TYPE_OF_VAGON_POSSESSION = '2'


class Fuel(enum.Enum):
    AB = 'AB'
    DT = 'DT'


class Cargo(enum.Enum):
    AB = '21105'
    DT = '21404'


class CargoWeight(enum.Enum):
    AB = '52'
    DT = '55'


@dataclass
class RailTariffSchema:
    rail_code_base_to: str
    rail_code_base_from: str
    weight: int
    cargo: int
    distance: int
    tarif: decimal.Decimal



class RailTariff(BaseModel):
    distance: int
    tarif: decimal.Decimal = Field(alias='sumtWithVat')





