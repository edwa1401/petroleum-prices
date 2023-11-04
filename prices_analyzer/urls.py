from django.urls import path

from prices_analyzer import views

app_name = 'prices_analyzer'

urlpatterns = [
    path('users/', views.users, name='users'),
    path('', views.PetroleumFilterView.as_view()),
]