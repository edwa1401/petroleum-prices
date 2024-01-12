from prices_analyzer.models import Prices
from rest_framework import serializers


# class PricesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Prices

#         fields = ['depot', 'production_place', 'rail_tariff', 'petroleum', 'full_price']

#         # fields = [
#         #     'petroleum__day',
#         #     'depot__name',
#         #     'production_place__name',
#         #     'petroleum__product_key__sort',
#         #     'petroleum__metric',
#         #     'petroleum__volume',
#         #     'petroleum__price',
#         #     'rail_tariff__tarif',
#         #     'full_price',
#         #     'rail_tariff__distance'
#         #     ]

class PricesSerializer(serializers.Serializer):
        day = serializers.DateField(source='petroleum.day')
        depot = serializers.CharField(source='depot.name', max_length=1000)
        production_place = serializers.CharField(
                source='production_place.name', max_length=1000
                )
        sort = serializers.CharField(
                source='petroleum.product_key.sort', max_length=1000
                )
        metric = serializers.CharField(source='petroleum.metric', max_length=1000)
        volume = serializers.DecimalField(
              source='petroleum.volume', max_digits=20, decimal_places=3
              )
        price_at_prodiction_place = serializers.DecimalField(
                source='petroleum.price', max_digits=20, decimal_places=2
                )
        rail_tariff = serializers.DecimalField(
              source='rail_tariff.tarif', max_digits=20, decimal_places=2
              )
        full_price = serializers.DecimalField(max_digits=20, decimal_places=2)
        distance_from_production_to_depot = serializers.CharField(
                source='rail_tariff.distance', max_length=1000)

        # fields = [
        #     'petroleum__day',
        #     'depot__name',
        #     'production_place__name',
        #     'petroleum__product_key__sort',
        #     'petroleum__metric',
        #     'petroleum__volume',
        #     'petroleum__price',
        #     'rail_tariff__tarif',
        #     'full_price',
        #     'rail_tariff__distance'
        #     ]
