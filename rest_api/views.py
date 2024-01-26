from django.http import HttpRequest, HttpResponse
from rest_api.models import PetroleumMap, PetroleumCode
from rest_api.serializers import PetroleumMapSerializer, PetroleumCodeSerializer
from rest_framework import generics
from rest_api.management.commands import petroleum_map_load


class PetroleumMapList(generics.ListCreateAPIView):
    queryset = PetroleumMap.objects.all()
    serializer_class = PetroleumMapSerializer

class PetroleumMapDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PetroleumMap.objects.all()
    serializer_class = PetroleumMapSerializer

class PetroleumCodeList(generics.ListCreateAPIView):
    queryset = PetroleumCode.objects.all()
    serializer_class = PetroleumCodeSerializer

class PetroleumCodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PetroleumCode.objects.all()
    serializer_class = PetroleumCodeSerializer



