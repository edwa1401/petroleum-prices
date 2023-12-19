import enum
from dataclasses import dataclass
from datetime import date


class PetroleumSort(enum.Enum):
    AI100 = 'AI100'
    AI98 = 'AI98'
    AI95 = 'AI95'
    AI92 = 'AI92'
    DTL = 'DTL'
    DTD = 'DTD'
    DTZ = 'DTZ'
    OTHER_PRODUCTS = 'Other products'


class Metric(enum.Enum):
    KG = 'Килограмм'
    TN = 'Метрическая тонна'


@dataclass(frozen=True, kw_only=True, slots=True)
class ProductKeySchema:
    name: str
    base: str
    base_name: str


@dataclass(frozen=True, kw_only=True, slots=True)
class ProductSchema:
    product_key: ProductKeySchema
    volume: float
    amount: float
    metric: str
    day: date


@dataclass(frozen=True, kw_only=True, slots=True)
class PetroleumSchema(ProductSchema):
    sort: PetroleumSort
    density: float

    @property
    def price(self) -> float | None:
        return round(self.amount / self.volume, 2) if self.amount and self.volume else None

    @property
    def retail_price(self) -> float | None:
        return round(self.price * self.density / 1000, 2) if self.price else None


