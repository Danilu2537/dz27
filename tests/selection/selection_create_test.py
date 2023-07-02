import pytest


@pytest.mark.django_db
def test_selection_create(client, access_token, ad_factory):
    ad_list = ad_factory.create_batch(4)
    data = {
        "name": "test_name",
        "items": [ad.id for ad in ad_list]
    }
    expected_data = {
        "id": 1,
        "name": "test_name",
        "owner": "test_user",
        "items": [ad.id for ad in ad_list]
    }
    response = client.post('/selection/', data=data, HTTP_AUTHORIZATION=f'Bearer {access_token}')
    assert response.data == expected_data
    assert response.data == expected_data
