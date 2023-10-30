from django.urls import path
from rail_tariff import views

urlpatterns = [
    path('', views.get_rail_tariff_view),
]