from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import generics, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response


from payment.models import (
    Reason, Payment, Collect, CollectPayment
)
from api.serializers import (
    ReasonSerializer,
    CollectSerializer,
    PaymentSerializer,
)

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

    def get_queryset(self):
        return Collect.objects.all()

    def get_serializer_class(self):
        return CollectSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PaymentViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    def get_queryset(self):
        return Payment.objects.all()

    def get_serializer_class(self):
        return PaymentSerializer

    def perform_create(self, serializer):
        serializer.save()
        payment = serializer.instance
        collect = get_object_or_404(
            Collect, pk=self.kwargs.get('collection_id'))
        CollectPayment.objects.create(collect=collect, payment=payment)
