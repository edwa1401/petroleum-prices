import pytest
from rail_tariff.models import RzdStation

from users.models import User


pytestmark = pytest.mark.django_db

# @pytest.mark.django_db
# class TestUsers:
#     pytestmark = pytest.mark.django_db
#     def test_my_user(self):
#         me = User.objects.get(username='admin')
#         assert me.is_superuser

# @pytest.mark.django_db
# def test_my_user():
#     me = User.objects.get(username='admin')
#     assert me.is_superuser

# def test_with_authenticated_client(client, django_user_model):
#     username = "user1"
#     password = "bar"
#     user = django_user_model.objects.create_user(username=username, password=password)
#     # client.force_login(user)
#     client.login(username=username, password=password)
#     response = client.get('/rail/rzdcode/create/')
#     assert response.content == ''

# # http://127.0.0.1:8000/accounts/login/?next=/rail/rzdstation/create/

# def test_an_admin_view(admin_client):
#     response = admin_client.get('/admin/')
#     assert response.status_code == 200

# @pytest.mark.django_db
# def test_path_to_parser_without_day(client):
#     response = client.get('/parser/')
#     assert response.content == b'No day in request'


def test_new_user(django_user_model):
    django_user_model.objects.create_user(username="someone", password="something")

@pytest.mark.django_db
def test_should_create_rzd_station(create_rzd_station):

    create_rzd_station(code='100500')

    assert RzdStation.objects.filter(code='100500').exists()


@pytest.mark.django_db
def test_success_check_rzd_station_name(create_rzd_station):

    new_station = create_rzd_station(station_name='Katsapetovka')

    assert new_station.station_name == 'Katsapetovka'
