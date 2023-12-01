from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from prices_analyzer.filters import PetroleumFilter
from prices_analyzer.services.create_prod_places import create_prod_places
from users.models import User
from prices_analyzer.models import Depot, Petroleum
from django_filters.views import FilterView # type: ignore[import]
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView

def users(request: HttpRequest) -> HttpResponse:
    users = User.objects.all()

    context = {
        'users': users,
    }
    return render(request, 'users.html', context=context)


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
    

class UpdateDepotView(UpdateView):
    model = Depot
    fields = ['name', 'user', 'rzd_code']
    template_name_suffix = '_update_form'


class DepotListView(ListView):
    model = Depot
