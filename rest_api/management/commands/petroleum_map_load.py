from pathlib import Path
import orjson
from rest_api.models import PetroleumMap


from django_typer import TyperCommand


class Command(TyperCommand):

    help = 'A command that uses Typer'

    def handle(self) -> None:
    
     petroleum_map = orjson.loads(Path('data/petroleums.json').read_bytes())
     for petroleum_sort, codes in petroleum_map.items():
          for code in codes:
               PetroleumMap.objects.create(sort=petroleum_sort, petroleum_code=code)


