from typing import Any

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db import transaction

from payment.factories import CollectWithGroupFactory

User = get_user_model()


class Command(BaseCommand):
    """Менеджмент команда для мок-даты."""

    @transaction.atomic
    def generate_users(self, amount: int):
        print('Приступаем к созданию!', flush=True)
        for i in range(1, amount+1):
            print(f'Создаем {i} объект!', flush=True)
            CollectWithGroupFactory.create()

    def add_arguments(self, parser):
        parser.add_argument(
            '-a',
            '--amount',
            action='store',
            default=10,
            help='Задание количества мок-даты.'
        )

    def handle(self, *args: Any, **options: Any) -> None:
        amount = int(options.get('amount')) or 10
        self.generate_users(amount=amount)
