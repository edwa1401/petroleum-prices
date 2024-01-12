from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from drf.models import Hallo
from drf.serializers import HalloSerializer
from rest_framework import generics



@csrf_exempt
def greet(request: HttpRequest) -> None:

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = HalloSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
#     elif request.method == 'GET':
#         greetings = Hallo.objects.all()
#         serializer = HalloSerializer(greetings, many=True)
#         return JsonResponse(serializer.data, safe=False)

# class GreetByName(generics.ListCreateAPIView):
#     greetings = Hallo.objects.all()
#     serializer_class = HalloSerializer
