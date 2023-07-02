import pytest

from ads.serializers import AdListSerializer, AdDetailSerializer


@pytest.mark.django_db
def test_ad_list(client, ad_factory):
    ad_list = sorted(ad_factory.create_batch(4), key=lambda x: x.price, reverse=True)
    response = client.get('/ad/')
    assert response.status_code == 200
    assert response.data == {
        'count': 4,
        'next': None,
        'previous': None,
        'results': AdListSerializer(ad_list, many=True).data
    }


