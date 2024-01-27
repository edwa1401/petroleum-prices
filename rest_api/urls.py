from django.urls import path
from rest_api import views

urlpatterns = [
    path('petroleum_maps/', views.PetroleumMapList.as_view()),
    path('petroleum_maps/<int:pk>/', views.PetroleumMapDetail.as_view()),
]

