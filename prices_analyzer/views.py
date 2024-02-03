import datetime
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from prices_analyzer.filters import PetroleumFilter
from prices_analyzer.services.create_prices import create_prices_for_all_depots_for_day
from prices_analyzer.services.create_prod_places import create_prod_places
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
    paginate_by = 10


def get_product_places_view(request: HttpRequest) -> HttpResponse:
    try:
        create_prod_places()
        result = 'success'
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





