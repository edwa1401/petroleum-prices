from django.urls import include, path
from rail_tariff import views

app_name = 'rail_tariff'
rzdcode_patterns = (
    [
    path('create/', views.CreateRzdCodeView.as_view()),
    path('<int:pk>/update/', views.UpdateRzdCodeView.as_view(), name='rzdcode-update'),
    path('<int:pk>/', views.RzdCodeDetailView.as_view(), name='detail')
],
'rzdcode'
)

tarif_patterns = (
    [
    path('create/', views.create_rail_tariff_view),
    path('get/', views.get_rail_tariff_view)
],
'tarif'
)

urlpatterns = [
    path('tarif/', include(tarif_patterns)),
    path('rzdcode/', include(rzdcode_patterns)),
]

