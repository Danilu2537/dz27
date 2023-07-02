import pytest


@pytest.fixture
@pytest.mark.django_db
def access_token(client, django_user_model):
    username = 'test_user'
    password = 'test_password'
    django_user_model.objects.create(username=username, password=password, is_active=True)
    response = client.post('/user/token/', data={'username': username, 'password': password})
    return response.data['access']
