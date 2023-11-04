import re
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


def get_sessid(session: requests.Session) -> str:
    URL_RZD = 'https://spimex.com/markets/oil_products/rzd/'
    response = session.get(URL_RZD)
    response_text = BeautifulSoup(response.text, 'html.parser')
    raw_scripts = response_text.head.find_all('script')
    for script in raw_scripts:
        if 'bitrix_sessid' in script.text:
            result = script.text
    sess_id_re = re.compile("^.*'bitrix_sessid':'(\w*)'.*$")
    match = sess_id_re.match(result)
    if match:
        sessid = match.groups()[0]
    return sessid


def get_rail_data_from_spimex(
        station_from: str,
        station_to: str,
        cargo: str,
        ves:str
        ) -> JsonResponse:
    
    session = requests.Session()
    session_id = get_sessid(session)

    ULR_TARIFF_CALCULATOR = 'https://spimex.com/local/components/spimex/calculator.rzd/templates/.default/ajax.php'

    payload = {
        'action': 'getCalculation',
        'sessid': session_id,
        'type': '43',
        'st1': station_from,
        'st2': station_to,
        'kgr': cargo,
        'ves': ves,
        'gp': '66',
        'nv': '1',
        'nvohr': '1',
        'nprov': '0',
        'osi': '4',
        'sv': '2',
    }
    response = session.post(url=ULR_TARIFF_CALCULATOR, data=payload)
    response.raise_for_status()

    return response.json()


def get_rail_tariff_view(request: HttpRequest) -> JsonResponse:
    station_to = request.GET.get('station_to')
    if not station_to:
        return JsonResponse({}, status=400)

    station_from = '223108'
    ''' razan_npz, basis_map.json'''
    cargo = '21105'
    ''' 21105 benzin, 21404 diesel '''

    ves = '52'
    ''' 52 bensin, 55 disel'''
    
    
    rzd_calc_response = get_rail_data_from_spimex(station_from, station_to, cargo, ves)
    distance = rzd_calc_response['data']['total']['distance']
    tariff = rzd_calc_response['data']['total']['sumtWithVat']
    

    content = {
        'distance': distance,
        'tariff': tariff
        }
    return JsonResponse(data=content)

