import pytest
from prices_analyzer.models import Depot
from rail_tariff.models import RzdStation

from users.models import User


pytestmark = pytest.mark.django_db

def test__authenticated_client__success(client, django_user_model):
    username = "user1"
    password = "12345"
    user = django_user_model.objects.create_user(username=username, password=password)
    # client.force_login(user)
    client.login(username=username, password=password)
    response = client.get('/accounts/login/')
    assert response.status_code == 200



def test__return_answer_path_to_parser_without_day__success(client):
    response = client.get('/parser/')
    assert response.content == b'No day in request'


@pytest.mark.django_db
def test__should_create_rzd_station__success(create_rzd_station):

    create_rzd_station(code='100500')

    assert RzdStation.objects.filter(code='100500').exists()


@pytest.mark.django_db
def test__check_rzd_station_name__success(create_rzd_station):

    new_station = create_rzd_station(station_name='Katsapetovka')

    assert new_station.station_name == 'Katsapetovka'


@pytest.mark.django_db
def test__should_create_depot__success(create_depot_db, create_signal_for_created_depot_mock):

    create_depot_db(name='Random depot')
    create_signal_for_created_depot_mock

    assert Depot.objects.filter(name='Random depot').exists()

# TODO вызывает сигнал WARNING  kombu.connection:connection.py:669 No hostname was supplied. Reverting to default 'localhost'
