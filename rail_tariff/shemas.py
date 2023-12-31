import decimal
import enum
import logging
import re
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field


logger = logging.getLogger(__name__)

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
    tarif: decimal.Decimal = Field(alias='sumtWithVat')


SPIMEX_RZD_CARGO_TYPE = '43'
SPIMEX_RZD_CARGO_TONNAGE = '66'
NUMBER_OF_VAGONS = '1'
NUMBER_OF_SECURED_VAGONS = '1'
NUMBER_OF_CONDUCTORS = '0'
NUMBER_OF_AXLES = '4'
TYPE_OF_VAGON_POSSESSION = '2'

class RailTariffClient:
    def __init__(self) -> None:
        self.session: requests.Session

    prefix = 'https://spimex.com'
    url_rzd = prefix + '/markets/oil_products/rzd/'
    url_tarif_calc = prefix + '/local/components/spimex/calculator.rzd/templates/.default/ajax.php'


    def _get_sessid_from_response(self, response: requests.Response) -> str:

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
    

    def get_session(self) -> str:
        
        self.session = requests.Session()
    
        response = self.session.get(self.url_rzd)
        logger.debug('Response headers=%s', response.headers)
        response.raise_for_status()

        return self._get_sessid_from_response(response)


    def get_rail_tariff(
            self,
            station_from: str,
            station_to: str,
            cargo: str,
            ves: str
            ) -> RailTariff:
        
        session_id = self.get_session()

        data = {
            'action': 'getCalculation',
            'sessid': session_id,
            'type': SPIMEX_RZD_CARGO_TYPE,
            'st1': station_from,
            'st2': station_to,
            'kgr': cargo,
            'ves': ves,
            'gp': SPIMEX_RZD_CARGO_TONNAGE,
            'nv': NUMBER_OF_VAGONS,
            'nvohr': NUMBER_OF_SECURED_VAGONS,
            'nprov': NUMBER_OF_CONDUCTORS,
            'osi': NUMBER_OF_AXLES,
            'sv': TYPE_OF_VAGON_POSSESSION,
        }
        response = self.session.post(url=self.url_tarif_calc, data=data)
        response.raise_for_status()

        payload = response.json()

        total = payload['data']['total']
        return RailTariff(**total)


