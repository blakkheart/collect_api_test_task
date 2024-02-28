from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, serializers, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
)
from django.db import transaction
from payment.models import (
    Reason, Payment, Collect, CollectPayment
)
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    ReasonSerializer,
    CollectSerializer,
    PaymentSerializer,
    CreateCollectSerializer,
)
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from api.tasks import send_email
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

User = get_user_model()


@extend_schema(
    tags=['Причины для сбора.']
)
class ReasonViewSet(viewsets.ViewSet):
    '''Вьюсет для создания причин сборов.'''

    @extend_schema(
        request=ReasonSerializer,
        responses={200: ReasonSerializer},
        description='Позволяет получить лист всех причин для пожертвования.'
    )
    def list(self, request):
        reasons = Reason.objects.all()
        serializer = ReasonSerializer(reasons, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=ReasonSerializer,
        responses={200: ReasonSerializer},
        description='Позволяет получить конкретную причину для пожертвования по id.'
    )
    def retrieve(self, request, pk=None):
        id = self.kwargs.get('pk')
        reason = get_object_or_404(Reason, pk=id)
        serializer = ReasonSerializer(reason)
        return Response(serializer.data)

    @extend_schema(
        request=ReasonSerializer,
        responses={201: ReasonSerializer, 404: status.HTTP_404_NOT_FOUND},
        description='Позволяет создать причину для пожертвования.'
    )
    @transaction.atomic
    def create(self, request):
        serializer = ReasonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Групповой сбор.']
)
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
        if self.action in ('list', ):
            return CollectSerializer
        return CreateCollectSerializer

    @extend_schema(
        request=CreateCollectSerializer,
        responses={201: CreateCollectSerializer},
        description=(
            'Позволяет создать Группой сбор.'
            'После создания сбора отправляется письмо на почту создавшему.'
        )
    )
    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        subject = 'Спасибо за огранизцию группового сбора!'
        message = (
            f'Привет! Спасибо за организацию {serializer.data.get("title")}\n'
            f'Держим кулачки, что сумму удастся собрать до {serializer.data.get("end_datetime")}'
        )
        recipients = [self.request.user.email]
        send_email.delay(subject, message, recipients)

    @extend_schema(
        request=CollectSerializer,
        responses={200: CollectSerializer},
        description='Позволяет получить лист всех Групповых сборов.'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(timeout=30))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@extend_schema(
    tags=['Платеж для сбора.']
)
class PaymentViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet
):
    '''Вьюсет для создания Платежа для сбора.'''

    def get_queryset(self):
        return Payment.objects.all()

    def get_serializer_class(self):
        return PaymentSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()
        payment = serializer.instance
        collect = get_object_or_404(
            Collect, pk=self.kwargs.get('collection_id'))
        collect.amount_collected += payment.amount
        if not collect.payments.filter(email_user=payment.email_user):
            collect.amount_of_people_donated += 1
        collect.save()
        CollectPayment.objects.create(collect=collect, payment=payment)
        subject = 'Спасибо за ваш денежный сбор!'
        message = (
            f'Привет! Спасибо за денежный сбор в размере {payment.amount}р.\n'
            f'Благодоря тебе, мы собрали уже {collect.amount_collected}р.!'
        )
        recipients = [payment.email_user]
        send_email.delay(subject, message, recipients)

    @method_decorator(cache_page(timeout=30))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserPayments(viewsets.ViewSet):
    '''Вьюсет для просмотра Платежей для сбора у пользователя.'''

    def list(self, request):
        user = request.user
        payment = Payment.objects.filter(email=user.email)
        serializer = PaymentSerializer(payment, many=True)
        return Response(serializer.data)
