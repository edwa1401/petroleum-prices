from django.urls import path
from drf.views import greet
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('hallo/', greet),
    # path('hallobyname/', GreetByName.as_view()),
]
# urlpatterns = format_suffix_patterns(urlpatterns)
