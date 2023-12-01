from django.urls import include, path

from prices_analyzer import views

app_name = 'prices_analyzer'

depot_pattern = (
    [
        path('create/', views.CreateDepotView.as_view()),
        path('', views.DepotListView.as_view(), name='list'),
    ], 
    'depot'
    )

urlpatterns = [
    path('users/', views.users, name='users'),
    path('', views.PetroleumFilterView.as_view()),
    path('prod/', views.get_product_places_view),
    path('depot/', include(depot_pattern))
]
