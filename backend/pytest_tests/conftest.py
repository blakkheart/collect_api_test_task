import tempfile

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
import pytest

from payment.models import Payment, Collect, CollectPayment, Reason


@pytest.fixture
def api_client():
    '''АПИ клиент.'''

    client = APIClient()
    return client


@pytest.fixture
def user_create_payload():
    '''Данные первого пользователя.'''

    payload = {
        'email': 'mail@example.com',
        'username': 'example3',
        'password': '3x4mpl345',
        'first_name': 'example_first',
        'last_name': 'example_last',
    }
    return payload


@pytest.fixture
def second_user_create_payload():
    '''Данные второго пользователя.'''

    payload = {
        'email': 'no_mail@example.com',
        'username': 'no_example3',
        'password': '3x4mpl345',
        'first_name': 'no_example_first',
        'last_name': 'no_example_last',
    }
    return payload


@pytest.fixture
def user_login_payload():
    '''Данные первого пользователя для токена.'''

    payload = {
        'email': 'mail@example.com',
        'password': '3x4mpl345',
    }
    return payload


@pytest.fixture
def collect_create_payload():
    '''Данные Группового сбора.'''

    payload = {
        'title': 'title',
        'reasons': {"title": "string"},
        'description': 'description',
        'amount_to_collect': 20000,
        'cover_image': 'iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAIAAADTED8xAAADMElEQVR4nOzVwQnAIBQFQYXff81RUkQCOyDj1YOPnbXWPmeTRef+/3O/OyBjzh3CD95BfqICMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMO0TAAD//2Anhf4QtqobAAAAAElFTkSuQmCC',
        'end_datetime': '2025-02-02 11:42:52',
    }
    return payload


@pytest.fixture
def reason_create_payload():
    '''Данные модели причин.'''

    payload = {
        'title': 'title',
    }
    return payload


@pytest.fixture
def reason_update_payload():
    '''Данные модели причин_другие.'''

    payload = {
        'title': 'new_title',
    }
    return payload


@pytest.fixture
def payment_create_payment_visible():
    '''Данные платежа видимого.'''

    payload = {
        'amount': 100,
        'invisible': False,
        'first_name_user': 'name',
        'last_name_user': 'last_name',
        'email_user': 'email@mail.ru',
    }
    return payload


@pytest.fixture
def payment_create_payment_invisible():
    '''Данные платежа невидимого.'''

    payload = {
        'amount': 100,
        'invisible': True,
        'first_name_user': 'name',
        'last_name_user': 'last_name',
        'email_user': 'email@mail.ru',
    }
    return payload


@pytest.fixture
def user_token(user_create):
    '''Получение токена для первого пользователя.'''

    Token.objects.create(user=user_create)
    return f'Token {user_create.auth_token.key}'


@pytest.fixture
def second_user_token(django_user_model, second_user_create_payload):
    '''Получение токена для второго пользователя.'''

    user = django_user_model.objects.create_user(**second_user_create_payload)
    Token.objects.create(user=user)
    return f'Token {user.auth_token.key}'


@pytest.fixture
def user_create(django_user_model, user_create_payload):
    '''Создание первого пользователя в БД.'''

    user = django_user_model.objects.create_user(**user_create_payload)
    return user


@pytest.fixture
def collect_create(user_create):
    '''Создание Группового платежа в БД.'''

    reason = Reason.objects.create(title='title')
    payload = {
        'author_id': user_create.id,
        'title': 'title',
        'reasons': reason,
        'description': 'description',
        'amount_to_collect': 20000,
        'cover_image': tempfile.NamedTemporaryFile(suffix=".jpg").name,
        'end_datetime': '2025-02-02 23:33:12TZ',
    }
    collect = Collect.objects.create(**payload)
    return collect


@pytest.fixture
def payment_create(payment_create_payment_visible):
    '''Создание платежа в БД.'''

    payment = Payment.objects.create(**payment_create_payment_visible)
    return payment
