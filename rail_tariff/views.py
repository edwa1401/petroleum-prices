from django.http import HttpRequest, JsonResponse
from django.shortcuts import render # noqa: F401
from rail_tariff.services.create_rail_tariff import get_rail_tariff_from_spimex



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
        'from': rail_tariff.rail_code_base_from,
        'to': rail_tariff.rail_code_base_to,
        'cargo': rail_tariff.cargo,
        'weight': rail_tariff.weight,
        'distance': rail_tariff.distance,
        'tariff': rail_tariff.tarif
        }
    return JsonResponse(data=content)


def create_rail_code_view(request: HttpRequest) -> JsonResponse:
    content: dict = {}
    return JsonResponse(data=content)
