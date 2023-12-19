
from pathlib import Path
from prices_analyzer.shemas import PetroleumSchema, PetroleumSort, ProductSchema
import orjson

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

    def convert(self, product: ProductSchema) -> PetroleumSchema:
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
