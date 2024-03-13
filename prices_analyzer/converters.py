
import decimal
import logging
from pathlib import Path

import orjson

from prices_analyzer.schemas import PetroleumSchema, PetroleumSort, ProductSchema
from rest_api.models import DensityMap, PetroleumMap

logger = logging.getLogger(__name__)


class PetroleumConverter:
    def __init__(self) -> None:
        self.petroleum_map: dict[str, PetroleumSort] = {}
        self.density_map: dict[PetroleumSort, float] = {}

    def _get_petroleums(self) -> dict[PetroleumSort, list[str]]:
        petroleums = orjson.loads(Path('data/petroleums.json').read_bytes())
        return {
            PetroleumSort[petroleum_sort]: codes
            for petroleum_sort, codes in petroleums.items()
        }

    def _get_density(self) -> dict[PetroleumSort, float]:
        density_map = orjson.loads(Path('data/density.json').read_bytes())
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

    def _convert_from_json(self, product: ProductSchema) -> PetroleumSchema:
        petroleum_sort = self._petroleum_map.get(
            product.product_key.name, PetroleumSort.OTHER_PRODUCTS
            )
        return PetroleumSchema(
            product_key=product.product_key,
            volume=product.volume,
            amount=product.amount,
            metric=product.metric,
            day=product.day,
            sort=petroleum_sort,
            density=self._density_map[petroleum_sort]
        )
    
    def convert(self, product: ProductSchema) -> PetroleumSchema:
        petroleum_sort = self.get_petroleum_sort(product)
        logger.debug('petroleum_sort=%s', petroleum_sort.value)
        density = self.get_density(petroleum_sort.value)

        return PetroleumSchema(
            product_key=product.product_key,
            volume=product.volume,
            amount=product.amount,
            metric=product.metric,
            day=product.day,
            sort=petroleum_sort,
            density=float(density),
        )
    
    def get_petroleum_sort(self, product: ProductSchema) -> PetroleumSort:

        petroleum_map = PetroleumMap.objects.all()
        
        sort = petroleum_map.filter(petroleum_code=product.product_key.name).first()
        if not sort:
            return PetroleumSort.OTHER_PRODUCTS

        return PetroleumSort[sort.sort]


    def get_density(self, petroleum_sort: str) -> decimal.Decimal:
        
        density = DensityMap.objects.get(sort=petroleum_sort)
        
        return density.density

