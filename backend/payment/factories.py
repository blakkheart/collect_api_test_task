import random

import factory
import pytz
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from factory.django import DjangoModelFactory

from payment.models import Collect, CollectPayment, Payment, Reason


User = get_user_model()


class UserFactory(DjangoModelFactory):
    '''Фабкрика пользователей.'''

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Sequence(lambda n: f'User-{n}')
    email = factory.Sequence(lambda n: f'email{n}@example.org')
    password = factory.Faker('password')

    class Meta:
        model = User
        django_get_or_create = ('username', )


class ReasonFactory(DjangoModelFactory):
    '''Фабкрика причин.'''

    title = factory.Faker('word')

    class Meta:
        model = Reason
        django_get_or_create = ('title',)


class PaymentFactory(DjangoModelFactory):
    '''Фабкрика платежей.'''

    amount = factory.Faker('random_int', min=10)
    invisible = factory.Faker('boolean')
    first_name_user = factory.Faker('first_name')
    last_name_user = factory.Faker('last_name')
    email_user = factory.Faker('email')

    class Meta:
        model = Payment


class CollectFactory(DjangoModelFactory):
    '''Фабкрика группового сбора.'''

    author = factory.SubFactory(UserFactory)
    title = factory.Faker(
        "sentence",
        nb_words=2,
        variable_nb_words=True
    )
    reasons = factory.SubFactory(ReasonFactory)
    description = factory.Faker(
        "sentence",
        nb_words=10,
        variable_nb_words=True
    )
    amount_to_collect = factory.Faker('random_number')
    cover_image = factory.LazyAttribute(
        lambda _: ContentFile(
            factory.django.ImageField()._make_data(
                {'width': 128, 'height': 128}
            ), 'example.jpg'
        )
    )
    end_datetime = factory.Faker('future_datetime', tzinfo=pytz.UTC)

    class Meta:
        model = Collect


class CollectPaymentFactory(DjangoModelFactory):
    '''Фабкрика для through модели сбора и платежей.'''

    collect = factory.SubFactory(CollectFactory)
    payment = factory.SubFactory(PaymentFactory)

    class Meta:
        model = CollectPayment
        django_get_or_create = ('collect', 'payment')


class CollectWithGroupFactory(CollectFactory):
    '''Фабрика для группового сбора с полем many-to-many.'''

    payments = factory.RelatedFactoryList(
        CollectPaymentFactory,
        factory_related_name='collect',
        size=lambda: random.randint(1, 10),
    )
