from django_filters import rest_framework as filters

from prices_analyzer.models import Prices

class PetroleumsFilter(filters.FilterSet):
    first_day = filters.DateFilter(field_name='petroleum__day', lookup_expr='gte')
    last_day = filters.DateFilter(field_name='petroleum__day', lookup_expr='lte')

    class Meta:
        model = Prices
        fields = ['depot', 'petroleum__product_key__sort', 'petroleum__metric',]
