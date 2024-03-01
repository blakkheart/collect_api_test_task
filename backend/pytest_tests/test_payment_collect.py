import pytest
from rest_framework import status


@pytest.mark.django_db
def test_check_payment_to_collection(
    api_client,
    user_create,
    user_token,
    collect_create,
    payment_create_payment_visible

):
    '''Проверка обновления Группового сбора после платежа.'''

    collect_id = collect_create.id

    url_create_payment = f'/api/v1/collections/{collect_id}/payments/'
    api_client.post(
        url_create_payment,
        payment_create_payment_visible,
        format='json',
        HTTP_AUTHORIZATION=user_token
    )
    url = f'/api/v1/collections/{collect_id}/'
    response = api_client.get(url)
    print((response.json()))
    assert len(response.json().get('payments')) == 1
    assert (
        collect_create.amount_collected
        + payment_create_payment_visible.get('amount')
        == response.json().get('amount_collected')
    )
    assert (
        collect_create.amount_of_people_donated
        + 1
        == response.json().get('amount_of_people_donated')
    )
