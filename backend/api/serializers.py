from django.contrib.auth import get_user_model
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from djoser.serializers import UserSerializer
from rest_framework import serializers


from payment.models import (
    Reason, Payment, Collect,
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
            'email_user',
        )
        read_only_fields = (
            'id',
            'donated_at',
        )

    def validate(self, data):
        user = self.context['request'].user
        if user.is_authenticated:
            data['first_name_user'] = user.first_name
            data['email_user'] = user.email
            data['last_name_user'] = user.last_name
        return data


class CreateCollectSerializer(serializers.ModelSerializer):
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
            'amount_of_people_donated',
            'cover_image',
            'end_datetime',
            'created_at',
            'payments',
        )
        read_only_fields = (
            'id',
            'author',
            'amount_collected',
            'amount_of_people_donated',
            'created_at',
            'payments',
        )

    @transaction.atomic
    def create(self, validated_data):
        reason_data = validated_data.pop('reasons')
        reason, _ = Reason.objects.get_or_create(**reason_data)
        return Collect.objects.create(reasons=reason, **validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        reason_data = validated_data.pop('reasons')
        reason, created = Reason.objects.get_or_create(**reason_data)
        instance.title = validated_data.get('title', instance.title)
        instance.reasons = reason if reason else instance.reason
        instance.description = validated_data.get(
            'description', instance.description)
        instance.amount_to_collect = validated_data.get(
            'amount_to_collect', instance.amount_to_collect)
        instance.cover_image = validated_data.get(
            'cover_image', instance.cover_image)
        instance.end_datetime = validated_data.get(
            'end_datetime', instance.end_datetime)
        instance.save()
        return instance


class CollectSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Группового денежного сбора.'''

    author = UserSerializer(read_only=True)
    reasons = ReasonSerializer()
    cover_image = Base64ImageField()

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
            'amount_of_people_donated',
            'cover_image',
            'end_datetime',
            'created_at',
        )
        read_only_fields = (
            'id',
            'author',
            'amount_collected',
            'amount_of_people_donated',
            'created_at',
        )
