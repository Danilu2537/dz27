import pytest

from ads.serializers import AdDetailSerializer


@pytest.mark.django_db
def test_ad_list(client, ad_factory, access_token):
    ad = ad_factory.create()
    response = client.get(f'/ad/{ad.id}/', HTTP_AUTHORIZATION=f'Bearer {access_token}')
    assert response.status_code == 200
    assert response.data == AdDetailSerializer(ad).data
