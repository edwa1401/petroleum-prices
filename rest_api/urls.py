from django.urls import path
from rest_api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('petroleum_maps/', views.PetroleumMapList.as_view()),
    path('petroleum_maps/<int:pk>/', views.PetroleumMapDetail.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)
