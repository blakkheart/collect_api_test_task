from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, serializers, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
)

from payment.models import (
    Reason, Payment, Collect, CollectPayment
)
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    ReasonSerializer,
    CollectSerializer,
    PaymentSerializer,
)
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from api.tasks import send_email

User = get_user_model()


class ReasonViewSet(viewsets.ViewSet):
    '''Вьюсет для создания причин сборов.'''

    def list(self, request):
        reasons = Reason.objects.all()
        serializer = ReasonSerializer(reasons, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        id = self.kwargs.get('pk')
        reason = get_object_or_404(Reason, pk=id)
        serializer = ReasonSerializer(reason)
        return Response(serializer.data)

    def create(self, request):
        serializer = ReasonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollectViewSet(viewsets.ModelViewSet):
    '''Вьюсет для создания Группового денежного сбора.'''
    http_method_names = ['get', 'post', 'delete', 'patch']
    permission_classes = (IsAuthorOrReadOnly, )

    def get_queryset(self):
        return (
            Collect.objects
            .select_related('author', 'reasons')
            .prefetch_related('payments')
        )

    def get_serializer_class(self):
        return CollectSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        subject = 'Спасибо за огранизцию группового сбора!'
        message = (
            f'Привет! Спасибо за организацию {serializer.data.get("title")}\n'
            f'Держим кулачки, что сумму удастся собрать до {serializer.data.get("end_datetime")}'
        )
        recipients = [self.request.user.email]
        send_email.delay(subject, message, recipients)

    @method_decorator(cache_page(timeout=30))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PaymentViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet
):
    '''Вьюсет для создания Платежа для сбора.'''
    # TODO : ordering
    # TODO : а нам вообще надо ли давать get запрос тут?

    def get_queryset(self):
        return Payment.objects.all()

    def get_serializer_class(self):
        return PaymentSerializer

    def perform_create(self, serializer):
        serializer.save()
        payment = serializer.instance
        collect = get_object_or_404(
            Collect, pk=self.kwargs.get('collection_id'))
        collect.amount_collected += payment.amount
        if not collect.payments.filter(email=payment.email):
            collect.amount_of_people_donated += 1
        collect.save()
        CollectPayment.objects.create(collect=collect, payment=payment)
        subject = 'Спасибо за ваш денежный сбор!'
        message = (
            f'Привет! Спасибо за денежный сбор в размере {payment.amount}р.\n'
            f'Благодоря тебе, мы собрали уже {collect.amount_collected}р.!'
        )
        recipients = [self.request.user.email]
        send_email.delay(subject, message, recipients)


class UserPayments(viewsets.ViewSet):
    '''Вьюсет для просмотра Платежей для сбора у пользователя.'''

    def list(self, request):
        user = request.user
        payment = Payment.objects.filter(email=user.email)
        serializer = PaymentSerializer(payment, many=True)
        return Response(serializer.data)
