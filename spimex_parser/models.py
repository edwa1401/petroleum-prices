from django.db import models
from django_extensions.db.models import TimeStampedModel


class TradeDay(TimeStampedModel, models.Model):
    day = models.DateField(blank=False)

    def __str__(self) -> str:
        return f'TradeDay for {self.day}'

class Section(TimeStampedModel, models.Model):
    name = models.CharField(max_length=1000, blank=False)
    metric = models.CharField(max_length=20, blank=False)
    trade_day = models.ForeignKey(TradeDay, on_delete=models.CASCADE, related_name='sections')

    def __str__(self) -> str:
        return f'Section: {self.name}, metric: {self.metric}, trade_day: {self.trade_day}'
    

class Contract(TimeStampedModel, models.Model):
    code = models.CharField(max_length=11, blank=False)
    name = models.CharField(max_length=1000, blank=False)
    base = models.CharField(max_length=1000, blank=False)
    volume = models.CharField(max_length=20, blank=False)
    amount = models.CharField(max_length=20, blank=False)
    price_change_amount = models.CharField(max_length=20, null=True, blank=True)
    price_change_ratio = models.CharField(max_length=20, null=True, blank=True)
    price_min = models.CharField(max_length=20, null=True, blank=True)
    price_avg = models.CharField(max_length=20, null=True, blank=True)
    price_max = models.CharField(max_length=20, null=True, blank=True)
    price_market = models.CharField(max_length=20, null=True, blank=True)
    price_best_bid = models.CharField(max_length=20, null=True, blank=True)
    price_best_call = models.CharField(max_length=20, null=True, blank=True)
    num_of_lots = models.SmallIntegerField(null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='contracts')


    def __str__(self) -> str:
        return f'Contract: {self.name}, basis: {self.base}, \
            volume: {self.volume}, amount: {self.amount}, section: {self.section}'
    


