import pytest


@pytest.mark.django_db
def test_ad_create(client, user, category, access_token):
    data = {
        "author": user.username,
        "category": category.name,
        "name": "test_long_name",
        "description": "test_description",
        "price": 100
    }
    expected_data = {
        "id": 1,
        "author": user.username,
        "category": category.name,
        "name": "test_long_name",
        "description": "test_description",
        "price": 100,
        "is_published": False,
        "image": None
    }
    response = client.post('/ad/', data=data, HTTP_AUTHORIZATION=f'Bearer {access_token}')
    assert response.data == expected_data
