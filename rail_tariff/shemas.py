import decimal
import enum
import re
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

from config import PAYLOAD_DATA


class Fuel(enum.Enum):
    AB = 'AB'
    DT = 'DT'


@dataclass
class RailTariffSchema:
    rail_code_base_to: int
    rail_code_base_from: int
    weight: int
    cargo: int
    distance: int
    tarif: decimal.Decimal

class SessionNotFoundError(Exception):
    pass



class RailTariff(BaseModel):
    distance: int
    tarif: decimal.Decimal = Field(alias='sumWithVat')


class RailTariffClient:
    def __init__(self) -> None:
        self.session: requests.Session


    url_rzd = 'https://spimex.com/markets/oil_products/rzd/'
    url_tarif_calc = 'https://spimex.com/local/components/spimex/calculator.rzd/templates/.default/ajax.php'


    def get_session(self) -> tuple[str, requests.Session]:
        
        session = requests.Session()
    
        response = session.get(self.url_rzd)
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
        return sessid, session

    def get_rail_tariff(
            self,
            station_from: str,
            station_to: str,
            cargo: str,
            ves: str
            ) -> RailTariff:
        
        session_id, session = self.get_session()

        data = {
            'action': 'getCalculation',
            'sessid': session_id,
            'type': PAYLOAD_DATA.get('type'),
            'st1': station_from,
            'st2': station_to,
            'kgr': cargo,
            'ves': ves,
            'gp': PAYLOAD_DATA.get('gp'),
            'nv': PAYLOAD_DATA.get('nv'),
            'nvohr': PAYLOAD_DATA.get('nvohr'),
            'nprov': PAYLOAD_DATA.get('nprov'),
            'osi': PAYLOAD_DATA.get('osi'),
            'sv': PAYLOAD_DATA.get('sv'),
        }
        response = session.post(url=self.url_tarif_calc, data=data)
        response.raise_for_status()

        payload = response.json()

        total = payload['data']['total']
        return RailTariff(**total)
