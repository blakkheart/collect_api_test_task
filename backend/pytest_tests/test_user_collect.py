'''Тестирование эндпоинта /user/collections/'''

import pytest
from rest_framework import status


@pytest.mark.django_db
def test_get_user_collections(
    api_client,
    user_create,
    user_token,
    collect_create,
):
    '''Получение Групповых сборов пользователя.'''

    url = f'/api/v1/user/{user_create.id}/collections/'
    response = api_client.get(url, HTTP_AUTHORIZATION=user_token)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_get_user_payments_noauth(
    api_client,
    user_create,
    collect_create,
):
    '''Получение Групповых сборов пользователя.'''

    url = f'/api/v1/user/{user_create.id}/collections/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
