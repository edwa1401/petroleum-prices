from django.db import models
from django_extensions.db.models import TimeStampedModel
from prices_analyzer.models import Petroleum, ProductKey


class PetroleumMap(TimeStampedModel, models.Model):
    sort = models.CharField(choices=ProductKey.Sort.choices, max_length=20, blank=False)

    def __str__(self) -> str:
        return f'petroleums sort {self.sort}'


class PetroleumCode(TimeStampedModel, models.Model):
    sort = models.ForeignKey(PetroleumMap, on_delete=models.PROTECT, related_name='codes')
    petroleum_code = models.CharField(max_length=4)

    def __str__(self) -> str:
        return f'petroleums sort {self.sort}code: {self.petroleum_code}'


class DensityMap(TimeStampedModel, models.Model):
    sort = models.CharField(choices=ProductKey.Sort.choices, max_length=20, blank=False)
    density = models.DecimalField(
        choices=Petroleum.Density.choices, max_digits=4, decimal_places=2, blank=True)
    
    def __str__(self) -> str:
        return f'petroleums sort {self.sort} density: {self.density}'

