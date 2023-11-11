import enum
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import orjson


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
class ProductKey_sh:
    name: str
    base: str
    base_name: str


@dataclass(frozen=True, kw_only=True, slots=True)
class Product_sh:
    product_key: ProductKey_sh
    volume: float
    amount: float
    metric: str
    day: date


@dataclass(frozen=True, kw_only=True, slots=True)
class Petroleum_sh(Product_sh):
    sort: PetroleumSort
    density: float

    @property
    def price(self) -> float | None:
        return round(self.amount / self.volume, 2) if self.amount and self.volume else None

    @property
    def retail_price(self) -> float | None:
        return round(self.price * self.density / 1000, 2) if self.price else None


class PetroleumConverter:
    def __init__(self) -> None:
        self.petroleum_map: dict[str, PetroleumSort] = {}
        self.density_map: dict[PetroleumSort, float] = {}

    def _get_petroleums(self) -> dict[PetroleumSort, list[str]]:
        petroleums = orjson.loads(Path('petroleums.json').read_bytes())
        return {
            PetroleumSort[petroleum_sort]: codes
            for petroleum_sort, codes in petroleums.items()
        }

    def _get_density(self) -> dict[PetroleumSort, float]:
        density_map = orjson.loads(Path('density.json').read_bytes())
        return {
            PetroleumSort[petroleum_sort]: density
            for petroleum_sort, density in density_map.items()
        }

    def load(self) -> None:
        petroleum = self._get_petroleums()
        self._petroleum_map = {
            key: petroleum_sort
            for petroleum_sort, product_keys in petroleum.items()
            for key in product_keys
        }
        self._density_map = self._get_density()

    def convert(self, product: Product_sh) -> Petroleum_sh:
        petroleum_sort = self._petroleum_map.get(
            product.product_key.name, PetroleumSort.OTHER_PRODUCTS
            )
        return Petroleum_sh(
            product_key=product.product_key,
            volume=product.volume,
            amount=product.amount,
            metric=product.metric,
            day=product.day,
            sort=petroleum_sort,
            density=self._density_map[petroleum_sort]
        )