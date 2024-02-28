from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_email(subject: str, message: str, recipients: list):
    '''Фукнция для отправки сообщений через celery.'''
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipients,
        fail_silently=False,
    )
