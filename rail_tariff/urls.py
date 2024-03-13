from django.urls import include, path
from rail_tariff import views

app_name = 'rail_tariff'

rzdstation_patterns = (
    [
    path('create/', views.CreateRzdCodeView.as_view()),
    path('<int:pk>/update/', views.UpdateRzdCodeView.as_view(), name='rzdstation-update'),
    path('<int:pk>/', views.RzdCodeDetailView.as_view(), name='detail')
],
'rzdstation'
)

tarif_patterns = (
    [
    path('create/', views.create_rail_tariff_view),
    path('create/<int:depot_id>/', views.create_rail_tariffs_for_depot),
    path('get/', views.get_rail_tariff_view)
],
'tarif'
)

urlpatterns = [
    path('tarif/', include(tarif_patterns)),
    path('rzdstation/', include(rzdstation_patterns)),
]

