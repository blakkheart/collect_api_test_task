'''Тестирование эндпоинта /reasons/'''

import pytest
from rest_framework import status

from payment.models import Reason


@pytest.mark.django_db
def test_get_reasons(
    api_client,
):
    url = '/api/v1/reasons/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_reasons_not_exist(
    api_client,
):
    url = '/api/v1/reasons/1/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_one_reason(
    api_client,
    user_token,
    reason_create_payload,
):
    url_create = '/api/v1/reasons/'
    response = api_client.post(
        url_create,
        reason_create_payload,
        format='json',
        HTTP_AUTHORIZATION=user_token
    )
    reason_id = response.json().get('id')
    url_get = f'/api/v1/reasons/{reason_id}/'
    response = api_client.get(url_get)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_reasons_auth(
    api_client,
    user_token,
    reason_create_payload,
):
    url_create = '/api/v1/reasons/'
    response = api_client.post(
        url_create,
        reason_create_payload,
        format='json',
        HTTP_AUTHORIZATION=user_token
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Reason.objects.count() == 1


@pytest.mark.django_db
def test_create_reasons_no_auth(
    api_client,
    reason_create_payload
):
    url_create = '/api/v1/reasons/'
    response = api_client.post(
        url_create,
        reason_create_payload,
        format='json',
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Reason.objects.count() == 0


@pytest.mark.django_db
def test_update_reasons(
    api_client,
    user_token,
    reason_create_payload,
    reason_update_payload,
):
    url_create = '/api/v1/reasons/'
    response = api_client.post(
        url_create,
        reason_create_payload,
        format='json',
        HTTP_AUTHORIZATION=user_token
    )
    reason_id = response.json().get('id')
    url_update = f'/api/v1/reasons/{reason_id}/'
    response = api_client.patch(
        url_update,
        reason_update_payload,
        format='json',
        HTTP_AUTHORIZATION=user_token
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_delete_reasons(
    api_client,
    user_token,
    reason_create_payload,
):
    url_create = '/api/v1/reasons/'
    response = api_client.post(
        url_create,
        reason_create_payload,
        format='json',
        HTTP_AUTHORIZATION=user_token
    )
    reason_id = response.json().get('id')
    url_delete = f'/api/v1/reasons/{reason_id}/'
    response = api_client.delete(
        url_delete, HTTP_AUTHORIZATION=user_token)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
