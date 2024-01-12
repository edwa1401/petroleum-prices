from rest_framework import serializers
from drf.models import Hallo


# class HalloSerializer(serializers.Serializer):
#     name = serializers.CharField(style={'base_template': 'textarea.html'})
#     msg = serializers.CharField(
#         required=False, allow_blank=True, max_length=100, style={'base_template': 'textarea.html'}
#         )
#     def create(self, validated_data):
#         return Hallo.objects.create(**validated_data)

class HalloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hallo
        fields = ['name', 'msg']
        