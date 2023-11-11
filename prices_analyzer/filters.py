import django_filters # type: ignore[import]
from prices_analyzer.models import Petroleum



class PetroleumFilter(django_filters.FilterSet):

    class Meta:
        model = Petroleum
        fields = {
            'sort': ['exact'],
            'base_name': ['exact'],
            'metric': ['exact'],
            'volume': ['gte'],
            'price': ['gte'],
            }
        