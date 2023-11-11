from django.db import models

from django_extensions.db.models import TimeStampedModel

class RailTariff(TimeStampedModel, models.Model):
    class Cargo(models.TextChoices):
        AB = 'AB'
        DT = 'DT'
        OTHER = 'OTHER'

    name_base_to = models.CharField(max_length=1000)
    rail_code_base_to = models.SmallIntegerField()
    name_base_from = models.CharField(max_length=1000)
    code_base_from = models.CharField(max_length=3)
    rail_code_base_from = models.SmallIntegerField()
    cargo = models.CharField(choices=Cargo.choices, max_length=5)
    distance = models.SmallIntegerField()
    tarif = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self) -> str:
        return f' from {self.name_base_to}, to {self.name_base_from}, \
             cargo: {self.cargo}, distance: {self.distance}, rail tariff: {self.tarif}'