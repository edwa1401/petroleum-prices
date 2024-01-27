from rest_framework import serializers
from rest_api.models import PetroleumMap


class PetroleumMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetroleumMap
        fields = ['sort', 'petroleum_code']
        

