from dataclasses import dataclass
import decimal
import re
from typing import Any
from bs4 import BeautifulSoup
import requests


@dataclass
class RailTariff_sh:
    rail_code_base_to: int
    rail_code_base_from: int
    weight: int
    cargo: int
    distance: int
    tarif: decimal.Decimal

class SessionNotFoundError(Exception):
    pass


class RailTariffGetter:
    def __init__(self, station_from: str, station_to: str, cargo: str, ves: str) -> None:
        self.station_from = station_from
        self.station_to = station_to
        self.cargo = cargo
        self.ves = ves


    def _get_sessid(self, session: requests.Session) -> str:
        URL_RZD = 'https://spimex.com/markets/oil_products/rzd/'
        response = session.get(URL_RZD)
        response.raise_for_status()

        response_text = BeautifulSoup(response.text, 'html.parser')
        if not response_text.head:
            raise SessionNotFoundError
        
        raw_scripts = response_text.head.find_all('script')
        for script in raw_scripts:
            if 'bitrix_sessid' in script.text:
                result = script.text
        sess_id_re = re.compile("^.*'bitrix_sessid':'(\w*)'.*$")
        match = sess_id_re.match(result)
        if match:
            sessid = match.groups()[0]
        return sessid

    def _get_rail_data_from_spimex(self) -> dict[str, Any]:
        
        session = requests.Session()
        session_id = self._get_sessid(session)

        ULR_TARIFF_CALCULATOR = 'https://spimex.com/local/components/spimex/calculator.rzd/templates/.default/ajax.php'

        payload = {
            'action': 'getCalculation',
            'sessid': session_id,
            'type': '43',
            'st1': self.station_from,
            'st2': self.station_to,
            'kgr': self.cargo,
            'ves': self.ves,
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
    
    def get_distance(self) -> str:
        return self._get_rail_data_from_spimex()['data']['total']['distance']
    
    def get_tarif(self) -> str:
        return self._get_rail_data_from_spimex()['data']['total']['sumtWithVat']
    
    def get_rail_tariff(self) -> RailTariff_sh:
        return RailTariff_sh(
            rail_code_base_to=int(self.station_to),
            rail_code_base_from=int(self.station_from),
            weight=int(self.ves),
            cargo=int(self.cargo),
            distance=int(self.get_distance()),
            tarif=decimal.Decimal(self.get_tarif())
        )
