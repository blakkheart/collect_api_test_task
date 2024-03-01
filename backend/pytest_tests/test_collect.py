'''Тестирование эндпоинта /collections/'''


import pytest
from rest_framework import status

from payment.models import Collect, Reason


@pytest.mark.django_db
def test_get_collections(api_client):
    '''Получение Групповых сборов.'''

    url = '/api/v1/collections/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_collection_auth(
    api_client,
    collect_create_payload,
    user_token
):
    '''Создание Группового сбора.'''

    url = '/api/v1/collections/'
    response = api_client.post(
        url,
        collect_create_payload,
        format='json',
        HTTP_AUTHORIZATION=user_token
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Collect.objects.count() == 1
    assert Reason.objects.count() == 1


@pytest.mark.django_db
def test_create_collection_no_auth(api_client, collect_create_payload):
    '''Создание Группового сбора без регистрации.'''

    url = '/api/v1/collections/'
    response = api_client.post(
        url,
        collect_create_payload,
        format='json',
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Collect.objects.count() == 0


@pytest.mark.django_db
def test_update_collection_author(
    api_client,
    collect_create_payload,
    user_token
):
    '''Обновление Группового сбора автором.'''

    url_create = '/api/v1/collections/'
    response = api_client.post(
        url_create,
        collect_create_payload,
        format='json',
        HTTP_AUTHORIZATION=user_token
    )
    collect_id = response.json().get('id')
    url_update = f'/api/v1/collections/{collect_id}/'
    update_payload = {
        'title': 'new_title',
    }
    response = api_client.patch(
        url_update,
        update_payload,
        format='json',
        HTTP_AUTHORIZATION=user_token
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('title') == 'new_title'


@pytest.mark.django_db
def test_update_collection_no_author(
    api_client,
    collect_create_payload,
    user_token,
    second_user_token
):
    '''Обновление Группового сбора не автором.'''

    url_create = '/api/v1/collections/'
    response = api_client.post(
        url_create,
        collect_create_payload,
        format='json',
        HTTP_AUTHORIZATION=user_token
    )
    collect_id = response.json().get('id')
    url_update = f'/api/v1/collections/{collect_id}/'
    update_payload = {
        'title': 'new_title',
    }
    response = api_client.patch(
        url_update,
        update_payload,
        format='json',
        HTTP_AUTHORIZATION=second_user_token
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_delete_collection_author(
    api_client,
    collect_create_payload,
    user_token,
):
    '''Удаление Группового сбора автором.'''

    url_create = '/api/v1/collections/'
    response = api_client.post(
        url_create,
        collect_create_payload,
        format='json',
        HTTP_AUTHORIZATION=user_token
    )
    collect_id = response.json().get('id')
    url_delete = f'/api/v1/collections/{collect_id}/'
    response = api_client.delete(
        url_delete,
        HTTP_AUTHORIZATION=user_token
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Collect.objects.count() == 0


@pytest.mark.django_db
def test_delete_collection_no_author(
    api_client,
    collect_create_payload,
    user_token,
    second_user_token
):
    '''Удаление Группового сбора не автором.'''

    url_create = '/api/v1/collections/'
    response = api_client.post(
        url_create,
        collect_create_payload,
        format='json',
        HTTP_AUTHORIZATION=user_token
    )
    collect_id = response.json().get('id')
    url_delete = f'/api/v1/collections/{collect_id}/'
    response = api_client.delete(
        url_delete,
        HTTP_AUTHORIZATION=second_user_token
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Collect.objects.count() == 1


@pytest.mark.django_db
def test_get_collection(
    api_client,
    collect_create_payload,
    user_token,
):
    '''Получение существующего Группового сбора.'''

    url_create = '/api/v1/collections/'
    response = api_client.post(
        url_create,
        collect_create_payload,
        format='json',
        HTTP_AUTHORIZATION=user_token
    )
    collect_id = response.json().get('id')
    url_delete = f'/api/v1/collections/{collect_id}/'
    response = api_client.get(url_delete)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_collection_not_exist(api_client):
    '''Получение несуществующего Группового сбора.'''

    url = '/api/v1/collections/1/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
