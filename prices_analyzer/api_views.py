import datetime
import logging

from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django.db.models.query import QuerySet
from rest_framework import generics

from prices_analyzer.models import Depot, Prices
from prices_analyzer.serializers import PricesSerializer
from prices_analyzer.services.create_prices import get_period_for_petroleums
from prices_analyzer.services.serialyzer import serialize_prices


logger = logging.getLogger(__name__)


def get_prices_for_period_view(request: HttpRequest) -> JsonResponse:

    raw_start_day = request.GET.get('start_day')
    raw_end_day = request.GET.get('end_day')
    raw_depot_id = request.GET.get('depot_id')

    if any ([raw_start_day, raw_end_day, raw_depot_id]) is None:

        return JsonResponse('BadRequest', status=400, safe=False)

    if raw_start_day and raw_end_day and raw_depot_id:
        start_day = datetime.datetime.strptime(raw_start_day, '%Y-%m-%d')
        end_day = datetime.datetime.strptime(raw_end_day, '%Y-%m-%d')
        depot_id=int(raw_depot_id)

    depot = Depot.objects.get(pk=depot_id)
    period = get_period_for_petroleums(start_date=start_day, end_date=end_day)

    prices = Prices.objects.filter(
        Q(petroleum__day__in=period),
        Q(depot=depot))
    

    if not prices:
        return JsonResponse({}, status=200, safe=False)

    
    view_prices = [serialize_prices(price) for price in prices]
    return JsonResponse(view_prices, status=200, safe=False)


class PricesListView(generics.ListAPIView):

    serializer_class = PricesSerializer

    def get_queryset(self) -> QuerySet[Prices]:
        prices = Prices.objects.all().prefetch_related('depot').prefetch_related(
            'petroleum').prefetch_related('production_place').prefetch_related('rail_tariff')

        raw_start_day = self.request.query_params.get('start_day')
        raw_end_day = self.request.query_params.get('end_day')
        depot_name = self.request.query_params.get('depot_name')

        if raw_start_day and raw_end_day and depot_name:
            start_day = datetime.datetime.strptime(raw_start_day, '%Y-%m-%d')
            end_day = datetime.datetime.strptime(raw_end_day, '%Y-%m-%d')

            period = get_period_for_petroleums(start_date=start_day, end_date=end_day)

            prices = prices.filter(
                Q(petroleum__day__in=period),
                Q(depot__name=depot_name))
            
        return prices

        



