from rest_api.models import PetroleumMap
from rest_api.serializers import PetroleumMapSerializer
from rest_framework import generics


class PetroleumMapList(generics.ListCreateAPIView):
    queryset = PetroleumMap.objects.all()
    serializer_class = PetroleumMapSerializer

class PetroleumMapDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PetroleumMap.objects.all()
    serializer_class = PetroleumMapSerializer



