import django_filters # type: ignore[import]
from prices_analyzer.models import Petroleum


class PetroleumFilter(django_filters.FilterSet):
    basis__name = django_filters.CharFilter(label='Basis')

    class Meta:
        model = Petroleum
        fields = {
            'product_key__sort': ['exact'],
            'basis__name': ['exact'],
            'metric': ['exact'],
            'volume': ['gte'],
            'price': ['lte'],
            'day': ['lte', 'gte']
            }