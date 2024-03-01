from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models, transaction

from payment.validators import validate_file_size


User = get_user_model()


class Reason(models.Model):
    '''Модель, описывающая причины сбора.'''
    title = models.CharField(
        max_length=40,
        validators=[MinLengthValidator(4)],
        verbose_name='Наименование причины сбора'
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Причина для сбора'
        verbose_name_plural = 'Причины для сбора'
        ordering = ['title']


class Payment(models.Model):
    '''Модель, описывающая Платеж для сбора.'''
    amount = models.PositiveIntegerField(
        verbose_name='Сумма платежа в рублях')
    donated_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        verbose_name='Дата поступления платежа')
    invisible = models.BooleanField(
        default=False, verbose_name='Скрыта ли сумма платежа')
    first_name_user = models.CharField(
        max_length=150, verbose_name='Имя пользователя, сделавшего платеж')
    last_name_user = models.CharField(
        max_length=150, verbose_name='Фамилия пользователя, сделавшего платеж')
    email_user = models.EmailField(
        max_length=254, verbose_name='Email пользователя, сделавшего платеж')

    def __str__(self) -> str:
        return f'{self.first_name_user} {self.last_name_user} donated {self.amount}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-donated_at']


class Collect(models.Model):
    '''Модель, описывающая Групповой денежный сбор.'''
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='collections',
        verbose_name='Автор сбора'
    )
    title = models.CharField(
        max_length=50, verbose_name='Наименование сбора')
    reasons = models.ForeignKey(
        Reason,
        on_delete=models.PROTECT,
        related_name='collections',
        verbose_name='Причина сбора'
    )
    description = models.TextField(verbose_name='Описание сбора')
    amount_to_collect = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Сколько надо собрать')
    amount_collected = models.PositiveIntegerField(
        default=0, verbose_name='Уже собрано')
    amount_of_people_donated = models.PositiveIntegerField(
        default=0, verbose_name='Количество людей, отправивших платеж')
    cover_image = models.ImageField(
        upload_to='covers/',
        validators=[validate_file_size],
        verbose_name='Обложка-изображение сбора'
    )
    end_datetime = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время окончания сбора'
    )
    created_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        verbose_name='Дата и время начала сбора'
    )
    payments = models.ManyToManyField(
        Payment,
        related_name='collections',
        through="CollectPayment",
        verbose_name='Платежи пользователей'
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Групповой сбор'
        verbose_name_plural = 'Групповые сборы'
        ordering = ['-created_at']


class CollectPayment(models.Model):
    '''Промежуточная модель для сбора и платежа.'''

    collect = models.ForeignKey(
        Collect,
        on_delete=models.PROTECT,
        related_name='collect_payments',
        verbose_name='Групповой сбор'
    )
    payment = models.ForeignKey(
        Payment,
        on_delete=models.PROTECT,
        related_name='collect_payments',
        verbose_name='Платеж пользователя'
    )

    def __str__(self) -> str:
        return f'{self.collect} + {self.payment}'

    @transaction.atomic
    def save(self, *args, **kwargs) -> None:
        '''Изменение Группового сбора с учетом поступившего платежа.'''

        self.collect.amount_collected += self.payment.amount
        if not self.collect.payments.filter(email_user=self.payment.email_user):
            self.collect.amount_of_people_donated += 1
        self.collect.save()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Групповой сбор и платеж'
        verbose_name_plural = 'Групповые сборы и платежи'
        ordering = ['-collect', 'payment']
