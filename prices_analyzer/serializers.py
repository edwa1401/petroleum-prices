from prices_analyzer.models import Prices
from rest_framework import serializers


class PricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = [
            'depot',
            'production_place',
            'rail_tariff',
            'petroleum',
            'full_price'
            ]

