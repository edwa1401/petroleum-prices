from django.urls import include, path
from prices_analyzer import api_views, views

app_name = 'prices_analyzer'

prices_pattern = (
    [
        path('', views.PricesListView.as_view(), name='list'),
        path('api/get/', api_views.get_prices_for_period_view),
        path('api/', api_views.PricesListView.as_view()),
        path('create/', views.create_prices_view),
    ], 
    'prices'
    )

depot_pattern = (
    [
        path('create/', views.CreateDepotView.as_view()),
        path('', views.DepotListView.as_view(), name='list'),
    ], 
    'depot'
    )

urlpatterns = [
    path('users/', views.users, name='users'),
    path('', views.index, name='index'),
    path('petroleums/', views.PetroleumFilterView.as_view()),
    path('petroleum/', views.PetroleumListFilterView.as_view(), name='petroleum_list'),
    path('prod/', views.get_product_places_view),
    path('depot/', include(depot_pattern)),
    path('prices/', include(prices_pattern)),
]
