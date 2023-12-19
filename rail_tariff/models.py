from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.urls import reverse


class RzdCode(TimeStampedModel, models.Model):
    code = models.SmallIntegerField(unique=True)
    station_name = models.CharField(max_length=1000, blank=True)

    def get_absolute_url(self) -> str:
        return reverse('rail_tariff:rzdcode:detail', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return f' Code {self.code}, station_name {self.station_name}'


class RailTariff(TimeStampedModel, models.Model):

    rail_code_base_to = models.ForeignKey(
        RzdCode, 
        on_delete=models.PROTECT,
        related_name='rail_codes_base_to'
        )
    rail_code_base_from = models.ForeignKey(
        RzdCode,
        on_delete=models.PROTECT,
        related_name='rail_codes_base_from'
        )
    weight = models.SmallIntegerField(choices=[(52, 'AB'), (55, 'DT')])
    cargo = models.SmallIntegerField(choices=[(21105, 'AB'), (21404, 'DT')])
    distance = models.SmallIntegerField()
    tarif = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self) -> str:
        return f' from {self.rail_code_base_from}, to {self.rail_code_base_to}, \
             cargo: {self.cargo}, distance: {self.distance}, rail tariff: {self.tarif}'
