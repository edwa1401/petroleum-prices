from django.urls import path
from spimex_parser import views

urlpatterns = [
    path('', views.trade_day_to_db_view,
         )
]