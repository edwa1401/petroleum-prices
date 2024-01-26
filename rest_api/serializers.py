from rest_framework import serializers
from rest_api.models import PetroleumMap, PetroleumCode


# class PetroleumMapSerializer(serializers.ModelSerializer):
#     petroleum_codes_
#     class Meta:
#         model = PetroleumMap
#         fields = ['sort']
        
class PetroleumCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PetroleumCode
        fields = ['sort', 'petroleum_code']

