from pathlib import Path
import orjson
from rest_api.models import DensityMap


from django_typer import TyperCommand


class Command(TyperCommand):

    help = 'A command that uses Typer'

    def handle(self) -> None:
    
     density_map = orjson.loads(Path('data/density.json').read_bytes())
     for petroleum_sort, density in density_map.items():
        DensityMap.objects.create(sort=petroleum_sort, density=density)
