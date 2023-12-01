from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView

from rail_tariff.models import RzdCode  # noqa: F401
from rail_tariff.services.create_rail_tariff import (
    get_rail_tariff_from_spimex,
    get_rail_tariffs_for_depot,
)
from rail_tariff.shemas import Fuel


class RzdCodeDetailView(DetailView):
    model = RzdCode
    template_name = 'rail_tariff/rzdcode_detail.html'


class CreateRzdCodeView(CreateView):
    model = RzdCode
    fields = ['code', 'station_name']


class UpdateRzdCodeView(UpdateView):
    model = RzdCode
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

    ves = '52'
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
    depot_id = request.GET.get('depot_id')
    fuel_type = request.GET.get('fuel')
    if not depot_id or not fuel_type:
        return HttpResponseBadRequest('Should be depot id and fuel')
    fuel = Fuel[fuel_type]
    
    
    get_rail_tariffs_for_depot(int(depot_id), fuel)

    return HttpResponse('succes')
    
