from django.urls import include, path
from rest_api import views

from users.views import UserViewSet, GroupViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'rzd_stations', views.RzdStationViewSet)
router.register(r'petroleums', views.PetroleumViewSet, basename='petroleums')
router.register(r'prices', views.PricesViewSet, basename='prices')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('petroleum_map/', views.PetroleumMapList.as_view()),
    path('petroleum_map/<int:pk>/', views.PetroleumMapDetail.as_view()),
    path('density_map/', views.DensityMapList.as_view()),
    path('density_map/<int:pk>/', views.DensityMapDetail.as_view()),
    path('production_places/', views.ProductionPlacesList.as_view()),
    path('production_places/<int:pk>/', views.ProductionPlaceDetail.as_view()),
    path('rzd_stations/', views.RzdStationListView.as_view()),
    path('rzd_station/create/', views.RzdStationCreateView.as_view()),
    path('rzd_station/<int:code>/', views.RzdStationUpdateView.as_view()),
    path('depot/', views.DepotCreateView.as_view()),
    path('depots/', views.DepotListView.as_view()),
    path('prices_two_weeks/', views.PricesUserListView.as_view()),
]

urlpatterns += router.urls
