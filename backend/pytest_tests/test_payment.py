'''Тестирование эндпоинта /collections/'''

import pytest
from rest_framework import status

from payment.models import Payment


@pytest.mark.django_db
def test_get_payments(api_client, collect_create):
    '''Получение платежей Группового сбора.'''

    url = f'/api/v1/collections/{collect_create.pk}/payments/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_payment_noauth_visible(
    api_client,
    collect_create,
    payment_create_payment_visible,
):
    '''Создание платежа Группового сбора без авторизации.'''

    url = f'/api/v1/collections/{collect_create.pk}/payments/'
    response = api_client.post(
        url,
        payment_create_payment_visible,
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Payment.objects.count() == 1


@pytest.mark.django_db
def test_create_payment_noauth_invisible(
    api_client,
    collect_create,
    payment_create_payment_invisible,
):
    '''Создание платежа Группового сбора без авторизации скрыто.'''

    url = f'/api/v1/collections/{collect_create.pk}/payments/'
    response = api_client.post(
        url,
        payment_create_payment_invisible,
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Payment.objects.count() == 1
    assert response.json().get('amount') == 'Hidden'


@pytest.mark.django_db
def test_create_payment_auth_(
    api_client,
    collect_create,
    payment_create_payment_visible,
    user_create_payload,
    user_token,
):
    '''Создание платежа Группового сбора с авторизацией.'''

    url = f'/api/v1/collections/{collect_create.pk}/payments/'
    response = api_client.post(
        url,
        payment_create_payment_visible,
        format='json',
        HTTP_AUTHORIZATION=user_token,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Payment.objects.count() == 1
    assert response.json().get('first_name_user') == user_create_payload.get('first_name')
    assert response.json().get('last_name_user') == user_create_payload.get('last_name')
    assert response.json().get('email_user') == user_create_payload.get('email')


@pytest.mark.django_db
def test_get_payment(
    api_client,
    collect_create,
    payment_create_payment_visible,
):
    '''Получение платежа Группового сбора.'''

    url_create = f'/api/v1/collections/{collect_create.pk}/payments/'
    response = api_client.post(
        url_create,
        payment_create_payment_visible,
        format='json',
    )
    payment_id = response.json().get('id')
    url_get = f'/api/v1/collections/{collect_create.pk}/payments/{payment_id}/'
    response = api_client.get(url_get)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_payment(
    api_client,
    collect_create,
    payment_create_payment_visible,
):
    '''Удаление платежа Группового сбора.'''

    url_create = f'/api/v1/collections/{collect_create.pk}/payments/'
    response = api_client.post(
        url_create,
        payment_create_payment_visible,
        format='json',
    )
    payment_id = response.json().get('id')
    url_get = f'/api/v1/collections/{collect_create.pk}/payments/{payment_id}/'
    response = api_client.patch(url_get, {'amount': 1000})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert Payment.objects.get(pk=payment_id).amount == 100


@pytest.mark.django_db
def test_delete_payment(
    api_client,
    collect_create,
    payment_create_payment_visible,
):
    '''Удаление платежа Группового сбора.'''

    url_create = f'/api/v1/collections/{collect_create.pk}/payments/'
    response = api_client.post(
        url_create,
        payment_create_payment_visible,
        format='json',
    )
    payment_id = response.json().get('id')
    url_get = f'/api/v1/collections/{collect_create.pk}/payments/{payment_id}/'
    response = api_client.delete(url_get)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert Payment.objects.count() == 1
