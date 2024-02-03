import pytest
from rail_tariff.models import RzdStation

from users.models import User


pytestmark = pytest.mark.django_db

# def test_with_authenticated_client(client, django_user_model):
#     username = "user1"
#     password = "bar"
#     user = django_user_model.objects.create_user(username=username, password=password)
#     # client.force_login(user)
#     client.login(username=username, password=password)
#     response = client.get('/rail/rzdcode/create/')
#     assert response.content == ''



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
