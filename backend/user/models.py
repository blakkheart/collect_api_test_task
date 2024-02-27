from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''Пользователь системы.'''
    middle_name = models.CharField(max_length=150, blank=True)
    birthdate = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
