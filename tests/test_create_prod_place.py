import pytest
from unittest.mock import patch, mock_open

from prices_analyzer.services.create_prod_places import create_prod_place_map

def test__create_prod_place_map__success():

    read_csv = "basis;rzd_code;prod_place;station\nabc;12345;town;station\ndef;67890;city;name"
    expected_dict = {'abc': ['12345', 'town', 'station'], 'def': ['67890', 'city', 'name']}

    with patch('prices_analyzer.services.create_prod_places.open', mock_open(
        read_data=read_csv)) as m:

        assert create_prod_place_map() == expected_dict

