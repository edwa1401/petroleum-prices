from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.urls import reverse


class RzdStation(TimeStampedModel, models.Model):
    code = models.CharField(max_length=20, unique=True)
    station_name = models.CharField(max_length=1000, blank=True)

    def get_absolute_url(self) -> str:
        return reverse('rail_tariff:rzdstation:detail', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return f' Code {self.code}, station_name {self.station_name}'


class RailTariff(TimeStampedModel, models.Model):

    rail_code_base_to = models.ForeignKey(
        RzdStation, 
        on_delete=models.PROTECT,
        related_name='rail_codes_base_to'
        )
    rail_code_base_from = models.ForeignKey(
        RzdStation,
        on_delete=models.PROTECT,
        related_name='rail_codes_base_from'
        )
    weight = models.SmallIntegerField(choices=[(52, 'AB'), (55, 'DT')])
    cargo = models.SmallIntegerField(choices=[(21105, 'AB'), (21404, 'DT')])
    distance = models.CharField(max_length=1000, blank=True)
    tarif = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self) -> str:
        return f' from {self.rail_code_base_from}, to {self.rail_code_base_to}, \
             cargo: {self.cargo}, distance: {self.distance}, rail tariff: {self.tarif}'
