import logging
import re

import requests
from bs4 import BeautifulSoup

from rail_tariff import schemas
from rail_tariff.errors import SessionNotFoundError


logger = logging.getLogger(__name__)


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
            ) -> schemas.RailTariff:
        
        session_id = self.get_session()

        data = {
            'action': 'getCalculation',
            'sessid': session_id,
            'type': schemas.SPIMEX_RZD_CARGO_TYPE,
            'st1': station_from,
            'st2': station_to,
            'kgr': cargo,
            'ves': ves,
            'gp': schemas.SPIMEX_RZD_CARGO_TONNAGE,
            'nv': schemas.NUMBER_OF_VAGONS,
            'nvohr': schemas.NUMBER_OF_SECURED_VAGONS,
            'nprov': schemas.NUMBER_OF_CONDUCTORS,
            'osi': schemas.NUMBER_OF_AXLES,
            'sv': schemas.TYPE_OF_VAGON_POSSESSION,
        }
        response = self.session.post(url=self.url_tarif_calc, data=data)
        response.raise_for_status()

        payload = response.json()

        total = payload['data']['total']
        return schemas.RailTariff(**total)
