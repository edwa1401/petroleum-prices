from django_filters import rest_framework as filters

from prices_analyzer.models import Petroleum, Prices

class PricesFilter(filters.FilterSet):
    day = filters.DateRangeFilter(field_name='petroleum__day')
    min_volume = filters.NumberFilter(field_name='petroleum__volume', lookup_expr='gte')

    class Meta:
        model = Prices
        fields = ['depot', 'petroleum__product_key__sort', 'petroleum__metric',]


class PetroleumFilter(filters.FilterSet):
    basis__name = filters.CharFilter(label='Basis')
    min_volume = filters.NumberFilter(field_name='volume', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    day = filters.DateFromToRangeFilter(field_name='day')

    class Meta:
        model = Petroleum
        fields = [
            'product_key__sort',
            'basis__name',
            'metric',
        ]

