import decimal
from django.db import models
from django_extensions.db.models import TimeStampedModel
from rail_tariff.models import RailTariff, RzdCode

from users.models import User


class ProductKey(TimeStampedModel, models.Model):
    
    class Sort(models.TextChoices):
        AI100 = 'AI100'
        AI98 = 'AI98'
        AI95 = 'AI95'
        AI92 = 'AI92'
        DTL = 'DTL'
        DTD = 'DTD'
        DTZ = 'DTZ'
        OTHER_PRODUCTS = 'Other products'

    code = models.CharField(max_length=4, blank=False)
    sort = models.CharField(choices=Sort.choices, max_length=20, blank=False)


class Basis(TimeStampedModel, models.Model):
    code = models.CharField(max_length=4, blank=False)
    name = models.CharField(max_length=1000, blank=True)
    def __str__(self) -> str:
        return f'Basis: code - {self.code}, name - {self.name}'
    
    
class ProductionPlace(TimeStampedModel, models.Model):
    basis = models.OneToOneField(Basis, on_delete=models.PROTECT)
    rzd_code = models.ForeignKey(RzdCode, on_delete=models.PROTECT)
    name = models.CharField(max_length=1000, blank=False)
    def __str__(self) -> str:
        return f' Basis code: {self.basis.code}, basis name: {self.basis.name}, \
            rzd code: {self.rzd_code.code}, production place name: {self.name}'    


class Depot(TimeStampedModel, models.Model):
    name = models.CharField(max_length=1000)
    user = models.ManyToManyField(User, related_name='depots')
    rzd_code = models.ForeignKey(RzdCode, on_delete=models.PROTECT)
    def __str__(self) -> str:
        return f' Petroleum depot: {self.name}'
    

class Petroleum(TimeStampedModel, models.Model):

    class Meta:
        get_latest_by = 'day'
        ordering = ['-day', 'price']

    class Density(decimal.Decimal, models.Choices):
        AB = 0.75
        DT = 0.84
        OTHER_PRODUCTS = 0.00

    class Metric(models.TextChoices):
        KG = 'Килограмм'
        TN = 'Метрическая тонна'

    product_key = models.ForeignKey(
        ProductKey, on_delete=models.RESTRICT, related_name='petroleums'
        )
    basis = models.ForeignKey(Basis, on_delete=models.RESTRICT, related_name='petroleums')
    volume = models.DecimalField(max_digits=20, decimal_places=3, null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    metric = models.CharField(choices=Metric.choices, max_length=20, blank=False)
    density = models.DecimalField(
         choices=Density.choices, max_digits=4, decimal_places=2, blank=True)
    day = models.DateField(blank=False)

    def __str__(self) -> str:
        return f'Petroleum: petroleum - {self.product_key.sort}, basis - {self.basis.name}, \
            volume - {self.volume}, price - {self.price}, metric - {self.metric}, \
                day - {self.day}'


class Prices(TimeStampedModel, models.Model):
    depot = models.ForeignKey(Depot, on_delete=models.PROTECT, related_name='prices')
    production_place = models.ForeignKey(
        ProductionPlace,
        on_delete=models.PROTECT,
        related_name='prices'
        )
    rail_tariff = models.ForeignKey(RailTariff, on_delete=models.PROTECT, related_name='prices')
    petroleum = models.ForeignKey(Petroleum, on_delete=models.PROTECT, related_name='prices')
    price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    def __str__(self) -> str:
        return f' Depot: {self.depot.name}, from {self.production_place.name}, \
             petroleum: {self.petroleum.product_key.sort}, distance: {self.rail_tariff.distance}, \
                price: {self.price}'
