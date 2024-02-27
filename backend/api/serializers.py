from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer as UserSerializerDjango
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from djoser.serializers import UserSerializer
from payment.models import (
    Reason, Payment, Collect, CollectPayment
)

User = get_user_model()


class ReasonSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели причин сбора.'''
    class Meta:
        model = Reason
        fields = (
            'id',
            'title',
        )
        read_only_fields = (
            'id',
        )


class PaymentSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Платеж для сбора.'''

    class Meta:
        model = Payment
        fields = (
            'id',
            'amount',
            'donated_at',
            'invisible',
            'first_name_user',
            'last_name_user',
            'middle_name_user',
            'email',
        )
        read_only_fields = (
            'id',
            'donated_at',
        )


class CollectSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Группового денежного сбора.'''

    author = UserSerializer(read_only=True)
    reasons = ReasonSerializer()
    cover_image = Base64ImageField()
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Collect
        fields = (
            'id',
            'author',
            'title',
            'reasons',
            'description',
            'amount_to_collect',
            'amount_collected',
            'anount_of_people_donated',
            'cover_image',
            'end_datetime',
            'payments',
        )
        read_only_fields = (
            'id',
            'author',
            'amount_collected',
            'anount_of_people_donated',
            'payments',
        )

    def create(self, validated_data):
        reason_data = validated_data.pop('reasons')
        reason = Reason.objects.create(**reason_data)
        return Collect.objects.create(reasons=reason, **validated_data)
