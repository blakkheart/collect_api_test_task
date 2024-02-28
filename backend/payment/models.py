from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

from payment.validators import validate_file_size

User = get_user_model()


class Reason(models.Model):
    '''Модель, описывающая причины сбора.'''
    title = models.CharField(
        max_length=40,
        validators=[MinLengthValidator(4)]
    )

    def __str__(self) -> str:
        return self.title


class Payment(models.Model):
    '''Модель, описывающая Платеж для сбора.'''
    amount = models.PositiveIntegerField()
    donated_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    invisible = models.BooleanField(default=False)

    first_name_user = models.CharField(max_length=150)
    last_name_user = models.CharField(max_length=150)
    email_user = models.EmailField(max_length=254)

    def __str__(self) -> str:
        return f'{self.first_name_user} {self.last_name_user} donated {self.amount}'

    class Meta:
        ordering = ['-donated_at']


class Collect(models.Model):
    '''Модель, описывающая Групповой денежный сбор.'''
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='collections')
    title = models.CharField(max_length=50)
    reasons = models.ForeignKey(
        Reason, on_delete=models.PROTECT, related_name='collections')
    description = models.TextField()
    amount_to_collect = models.PositiveIntegerField(null=True, blank=True)
    amount_collected = models.PositiveIntegerField(default=0)
    amount_of_people_donated = models.PositiveIntegerField(default=0)
    cover_image = models.ImageField(
        upload_to='covers/', validators=[validate_file_size])
    end_datetime = models.DateTimeField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    payments = models.ManyToManyField(
        Payment, related_name='collections', through="CollectPayment")

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['-created_at']


class CollectPayment(models.Model):
    collect = models.ForeignKey(
        Collect, on_delete=models.PROTECT, related_name='collect_payments')
    payment = models.ForeignKey(
        Payment, on_delete=models.PROTECT, related_name='collect_payments')

    def __str__(self) -> str:
        return f'{self.collect} + {self.payment}'
