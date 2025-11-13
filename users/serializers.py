import django_filters
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import Payment, User
from users.services import get_content_type_by_name


class PaymentFilter(django_filters.FilterSet):
    payment_method = django_filters.CharFilter(lookup_expr="iexact")
    paid_object = django_filters.CharFilter(method="filter_object_type")

    def filter_object_type(self, queryset, name, value):
        content_type = get_content_type_by_name(value)
        return queryset.filter(content_type=content_type)

    class Meta:
        model = Payment
        fields = ["paid_object", "object_id", "payment_method"]


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = (
            "amount",
            "stripe_session_id",
            "payment_link",
            "payment_status",
            "stripe_payment_intent_id",
            "user",
            "date",
        )

    def validate(self, attrs):
        """Проверяем, что оплачиваемый объект существует и имеет цену"""
        content_type = attrs.get("content_type")
        object_id = attrs.get("object_id")

        if content_type and object_id:
            try:
                # Получаем объект (курс или урок)
                paid_object = content_type.get_object_for_this_type(id=object_id)

                # Проверяем, что у объекта есть цена
                if not hasattr(paid_object, "price"):
                    raise serializers.ValidationError("У выбранного объекта нет цены")

                # Проверяем, что цена больше 0
                if paid_object.price <= 0:
                    raise serializers.ValidationError("Цена объекта должна быть больше 0")

            except ObjectDoesNotExist:
                raise serializers.ValidationError("Объект для оплаты не найден")

        return attrs

    def create(self, validated_data):
        """Автоматически устанавливаем пользователя из запроса"""
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class UserSerializer(ModelSerializer):
    payments = SerializerMethodField()

    def get_payments(self, user):
        payments = user.payments.all()
        return PaymentSerializer(payments, many=True).data

    class Meta:
        model = User
        fields = "__all__"


class UserPublicSerializer(ModelSerializer):
    payments = SerializerMethodField()

    def get_payments(self, user):
        payments = user.payments.all()
        return PaymentSerializer(payments, many=True).data

    class Meta:
        model = User
        exclude = (
            "password",
            "last_login",
            "last_name",
            "is_superuser",
            "payments",
        )
