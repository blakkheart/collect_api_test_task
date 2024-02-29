from typing import Any

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db import transaction

from payment.factories import CollectWithGroupFactory, UserFactory

User = get_user_model()


class Command(BaseCommand):
    """Менеджмент команда для мок-даты."""

    @transaction.atomic
    def generate_users(self, amount: int):
        UserFactory.create_batch(amount)
        CollectWithGroupFactory.create_batch(amount)

    def add_arguments(self, parser):
        parser.add_argument(
            '-a',
            '--amount',
            action='store',
            default=10,
            help='Задание количество мок-даты.'
        )

    def handle(self, *args: Any, **options: Any) -> None:
        amount = int(options.get('amount')) or 10
        self.generate_users(amount=amount)
