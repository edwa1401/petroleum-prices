from django.urls import path

from prices_analyzer import views

app_name = 'prices_analyzer'

urlpatterns = [
    path('', views.index, name='index'),
]