from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from rail_tariff.models import RzdStation
from rail_tariff.services.create_rail_tariff import (
    get_rail_tariff_from_spimex,
    get_tariffs_for_all_depots,
    get_rail_tariffs_for_depot
)

class RzdCodeDetailView(DetailView):
    model = RzdStation
    template_name = 'rail_tariff/rzdstation_detail.html'


class CreateRzdCodeView(LoginRequiredMixin, CreateView):
    model = RzdStation
    fields = ['code', 'station_name']


class UpdateRzdCodeView(LoginRequiredMixin, UpdateView):
    model = RzdStation
    fields = ['code', 'station_name']
    template_name_suffix = '_update_form'


def get_rail_tariff_view(request: HttpRequest) -> JsonResponse:
    station_to = request.GET.get('station_to')
    if not station_to:
        return JsonResponse({}, status=400)
    
    '''188205 = Калуга'''
    ''' 060073 МОСКВА-ПАССАЖИРСКАЯ'''

    station_from = '223108'
    ''' razan_npz, basis_map.json'''
    ''' https://vagon1520.ru/stations '''
    cargo = '21105'
    ''' 21105 benzin, 21404 diesel '''

    ves = '55'
    ''' 52 bensin, 55 disel'''

    rail_tariff = get_rail_tariff_from_spimex(
        station_to=station_to,
        station_from=station_from,
        cargo=cargo,
        ves=ves
    )

    content = {
        'from': station_from,
        'to': station_to,
        'cargo': cargo,
        'weight': ves,
        'distance': rail_tariff.distance,
        'tariff': rail_tariff.tarif
        }
    return JsonResponse(data=content)


def create_rail_tariff_view(request: HttpRequest) -> HttpResponse:
    
    get_tariffs_for_all_depots()

    return HttpResponse('succes')
    
def create_rail_tariffs_for_depot(request: HttpRequest) -> HttpResponse:
    depot_id = request.GET.get('depot_id')
    if not depot_id:
        return HttpResponseBadRequest('should be depots id')

    
    get_rail_tariffs_for_depot(depot_id=int(depot_id))

    return HttpResponse('succes')
