from django.urls import path
from rail_tariff import views

urlpatterns = [
    path('tarif/', views.get_rail_tariff_view),
    path('code/', views.create_rail_code_view),
]
