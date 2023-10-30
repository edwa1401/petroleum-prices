from django.db import models
from django_extensions.db.models import TimeStampedModel



class Petroleum(TimeStampedModel, models.Model):

    class PetroleumSort(models.TextChoices):
        AI100 = 'AI100'
        AI98 = 'AI98'
        AI95 = 'AI95'
        AI92 = 'AI92'
        DTL = 'DTL'
        DTD = 'DTD'
        DTZ = 'DTZ'
        OTHER_PRODUCTS = 'Other products'

    class Metric(models.TextChoices):
        KG = 'Килограмм'
        TN = 'Метрическая тонна'

    product_key = models.CharField(max_length=4, blank=False)
    base = models.CharField(max_length=3, blank=False)
    base_name = models.CharField(max_length=1000, blank=False)
    volume = models.SmallIntegerField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    metric = models.CharField(choices=Metric.choices, max_length=20, blank=False)
    day = models.DateField(blank=False)
    sort = models.CharField(choices=PetroleumSort.choices, max_length=15, blank=False)
    density = models.DecimalField(max_digits=4, decimal_places=2)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self) -> str:
        return f'Petroleum: product_key - {self.product_key}, base - {self.base_name}, \
            volume - {self.volume}, price - {self.price}, metric - {self.metric}, day - {self.day}'
    
        
        
