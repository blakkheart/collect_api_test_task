from typing import Any

from django.db import transaction
from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

from payment.factories import (
    UserFactory, CollectWithGroupFactory,
)

User = get_user_model()


class Command(BaseCommand):
    """Менеджмент команда для мок-даты."""

    @transaction.atomic
    def generate_users(self, amount: int):
        UserFactory.create_batch(amount)
        CollectWithGroupFactory.create_batch(amount)

    def handle(self, *args: Any, **options: Any) -> None:
        amount = options.get('amount') or 10
        self.generate_users(amount=amount)
