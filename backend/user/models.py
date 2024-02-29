from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''Пользователь системы.'''

    email = models.EmailField(unique=True, verbose_name='Email пользователя')
    first_name = models.CharField(
        max_length=150, verbose_name='Имя пользователя')
    last_name = models.CharField(
        max_length=150, verbose_name='Фамилия пользователя')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']
