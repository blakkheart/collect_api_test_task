'''Тестирование эндпоинта /user/payments/'''

import pytest
from rest_framework import status


@pytest.mark.django_db
def test_get_user_payments(
    api_client,
    user_create,
    user_token,
    collect_create,
    payment_create_payment_visible,
):
    '''Получение платежей пользователя.'''

    url = f'/api/v1/collections/{collect_create.pk}/payments/'
    response = api_client.post(
        url,
        payment_create_payment_visible,
        format='json',
        HTTP_AUTHORIZATION=user_token,
    )
    url = f'/api/v1/user/{user_create.id}/payments/'
    response = api_client.get(url, HTTP_AUTHORIZATION=user_token)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_get_user_payments_noauth(
    api_client,
    payment_create_payment_visible,
    collect_create,
    user_token,
    user_create
):
    '''Получение платежей пользователя.'''

    url = f'/api/v1/collections/{collect_create.pk}/payments/'
    response = api_client.post(
        url,
        payment_create_payment_visible,
        format='json',
        HTTP_AUTHORIZATION=user_token,
    )
    url = f'/api/v1/user/{user_create.id}/payments/'

    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
