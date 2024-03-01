'''Тестирование регистрации пользователя.'''

from django.contrib.auth import get_user_model
import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token


User = get_user_model()


@pytest.mark.django_db
def test_create_user(api_client, user_create_payload):
    '''Тестирование регистрации пользователя.'''

    url = '/api/v1/auth/users/'
    response = api_client.post(url, user_create_payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_create_user_with_no_last_name(api_client):
    '''Тестирование регистрации без параметра.'''

    url = '/api/v1/auth/users/'
    payload = {
        'email': 'mail@example.com',
        'username': 'example3',
        'password': '3x4mpl345',
        'first_name': 'example_first',
    }
    response = api_client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_create_user_with_no_first_name(api_client):
    '''Тестирование регистрации без параметра.'''

    url = '/api/v1/auth/users/'
    payload = {
        'email': 'mail@example.com',
        'username': 'example3',
        'password': '3x4mpl345',
        'last_name': 'example_last',
    }
    response = api_client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_create_user_with_no_email(api_client):
    '''Тестирование регистрации без параметра.'''

    url = '/api/v1/auth/users/'
    payload = {
        'username': 'example3',
        'password': '3x4mpl345',
        'firts_name': 'example_first',
        'last_name': 'example_last',
    }
    response = api_client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_create_user_with_no_username(api_client):
    '''Тестирование регистрации без параметра.'''

    url = '/api/v1/auth/users/'
    payload = {
        'email': 'mail@example.com',
        'password': '3x4mpl345',
        'firts_name': 'example_first',
        'last_name': 'example_last',
    }
    response = api_client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_create_user_with_no_password(api_client):
    '''Тестирование регистрации без параметра.'''

    url = '/api/v1/auth/users/'
    payload = {
        'email': 'mail@example.com',
        'username': 'example3',
        'firts_name': 'example_first',
        'last_name': 'example_last',
    }
    response = api_client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_login_user(api_client, user_create_payload, user_login_payload):
    '''Тестирование получение токена для пользователя.'''

    url_create = '/api/v1/auth/users/'
    api_client.post(url_create, user_create_payload, format='json')
    url_login = '/api/v1/auth/token/login'
    response = api_client.post(url_login, user_login_payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert Token.objects.count() == 1


@pytest.mark.django_db
def test_login_user_with_no_password(
    api_client,
    user_create_payload,
):
    '''Тестирование получение токена пользователя с неверными параметрами.'''

    url_create = '/api/v1/auth/users/'
    api_client.post(url_create, user_create_payload, format='json')
    url_login = '/api/v1/auth/token/login'
    login_payload = {
        'email': 'mail@example.com',
    }
    response = api_client.post(url_login, login_payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Token.objects.count() == 0


@pytest.mark.django_db
def test_login_user_with_no_email(
    api_client,
    user_create_payload,
):
    '''Тестирование получение токена пользователя с неверными параметрами.'''

    url_create = '/api/v1/auth/users/'
    api_client.post(url_create, user_create_payload, format='json')
    url_login = '/api/v1/auth/token/login'
    login_payload = {
        'username': 'no_example3',
        'password': '3x4mpl345',
    }
    response = api_client.post(url_login, login_payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Token.objects.count() == 0
