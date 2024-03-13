import datetime
from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from prices_analyzer.filters import PetroleumFilter
from prices_analyzer.services.create_prices import create_prices_for_all_depots_for_day
from prices_analyzer.services.create_prod_places import update_prod_places
from prices_analyzer.models import Depot, Petroleum, Prices
from django_filters.views import FilterView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from spimex_parser.models import TradeDay
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


def users(request: HttpRequest) -> HttpResponse:
    users = User.objects.all()

    context = {
        'users': users,
    }
    return render(request, 'users.html', context=context)


def index(request: HttpRequest) -> HttpResponse:

    num_trade_days = TradeDay.objects.all().count()
    num_depots = Depot.objects.all().count()

    context = {
        'num_trade_days': num_trade_days,
        'num_depots': num_depots,
    }

    return render(request, 'index.html', context=context)


class PetroleumFilterView(FilterView):
    model = Petroleum
    filterset_class = PetroleumFilter
    template_name = 'petroleum_filter.html'
    paginate_by = 5
    context_object_name = 'petroleums'

    
class PetroleumListFilterView(ListView):
    model = Petroleum
    template_name = 'petroleum_list.html'
    paginate_by = 5
    context_object_name = 'petroleums'

    
    def get_queryset(self) -> QuerySet[Any]:
        petroleum_sort_filter = self.request.GET.get('petroleum_sort_filter')
        basis_name_filter = self.request.GET.get('basis_name_filter')
        metric_filter = self.request.GET.get('metric_filter')
        volume_filter = self.request.GET.get('volume_filter')
        price_filter = self.request.GET.get('price_filter')
        min_day_filter = self.request.GET.get('min_day_filter')
        max_day_filter = self.request.GET.get('max_day_filter')

        qs = Petroleum.objects.all().prefetch_related('product_key').prefetch_related('basis')

        if petroleum_sort_filter:
            qs = qs.filter(product_key__sort=petroleum_sort_filter)

        if basis_name_filter:
            qs = qs.filter(basis__name=basis_name_filter)

        if metric_filter:
            qs = qs.filter(metric=metric_filter)
        
        if volume_filter:
            qs = qs.filter(volume__gte=volume_filter)
        
        if price_filter:
            qs = qs.filter(price__lte=price_filter)

        if min_day_filter:
            qs = qs.filter(day__gte=min_day_filter)

        if max_day_filter:
            qs = qs.filter(day__lte=max_day_filter)

        qs = qs.filter()
        return qs


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['petroleum_sort_filter:'] = self.request.GET.get('petroleum_sort_filter:')
        context['basis_name_filter'] = self.request.GET.get('basis_name_filter')
        context['metric_filter'] = self.request.GET.get('metric_filter')
        context['volume_filter'] = self.request.GET.get('volume_filter')
        context['price_filter'] = self.request.GET.get('price_filter')
        context['min_day_filter'] = self.request.GET.get('min_day_filter')
        context['max_day_filter'] = self.request.GET.get('max_day_filter')
        return context


def get_product_places_view(request: HttpRequest) -> HttpResponse:
    try:
        update_prod_places()
        result = 'prod_places_successfully_updated'
    except (TypeError, ValueError) as e:
        result = f'incorrect data format {e}'

    return HttpResponse(result)


class CreateDepotView(CreateView):
    model = Depot
    fields = ['name', 'user', 'rzd_code']
# дополнительно должна вызываться вьюха с get tafiff for depot
# следом должны создаться prices для всех petroleums в базе для этого depot


class UpdateDepotView(UpdateView):
    model = Depot
    fields = ['name', 'user', 'rzd_code']
    template_name_suffix = '_update_form'


class DepotListView(ListView):
    model = Depot


class PricesListView(LoginRequiredMixin, ListView):
    model = Prices


def create_prices_view(request: HttpRequest) -> HttpResponse:
    raw_day = request.GET.get('day')
    if not raw_day:
        return HttpResponseBadRequest('should be day')
    
    day = datetime.datetime.strptime(raw_day, '%Y-%m-%d')

    create_prices_for_all_depots_for_day(day)
    result = 'success'

    return HttpResponse(result)





