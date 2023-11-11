from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from prices_analyzer.filters import PetroleumFilter
from users.models import User
from prices_analyzer.models import Petroleum
from django_filters.views import FilterView # type: ignore[import]

def users(request: HttpRequest) -> HttpResponse:
    users = User.objects.all()

    context = {
        'users': users,
    }
    return render(request, 'index.html', context=context)


class PetroleumFilterView(FilterView):
    model = Petroleum
    filterset_class = PetroleumFilter
    template_name = 'petroleum_filter.html'
    paginate_by = 10






