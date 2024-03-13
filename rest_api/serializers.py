from rest_framework import serializers
from prices_analyzer.models import Depot, ProductionPlace
from rail_tariff.models import RzdStation
from rest_api.models import PetroleumMap, DensityMap


class PetroleumMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetroleumMap
        fields = ['sort', 'petroleum_code']


class DensityMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = DensityMap
        fields = ['sort', 'density']


class ProductionPlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionPlace
        fields = ['basis', 'rzd_code', 'name']


class DepotSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Depot
        fields = ['name', 'rzd_code', 'user']


class RzdStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RzdStation
        fields = ['code', 'station_name']


