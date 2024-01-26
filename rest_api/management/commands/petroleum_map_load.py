from pathlib import Path
import orjson
from rest_api.models import PetroleumCode, PetroleumMap


from django_typer import TyperCommand


class Command(TyperCommand):

    help = 'A command that uses Typer'

    def handle(self) -> None:
    
     petroleum_map = orjson.loads(Path('data/petroleums.json').read_bytes())
     for petroleum_sort, codes in petroleum_map.items():
          sort = PetroleumMap.objects.create(sort=petroleum_sort)
          for code in codes:
               PetroleumCode.objects.create(sort=sort, petroleum_code=code)


