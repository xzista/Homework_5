import django_filters
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class PaymentFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(fields=(("date", "date"),))

    payment_method = django_filters.CharFilter(lookup_expr="iexact")

    paid_object = django_filters.CharFilter(method="filter_object_type")

    def filter_object_type(self, queryset, name, value):
        if value == "course":
            return queryset.filter(content_type_id=7)
        elif value == "lesson":
            return queryset.filter(content_type_id=8)
        return queryset

    class Meta:
        model = Payment
        fields = ["paid_object", "object_id", "payment_method"]


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    payments = SerializerMethodField()

    def get_payments(self, user):
        payments = user.payments.all()
        return PaymentSerializer(payments, many=True).data

    class Meta:
        model = User
        exclude = (
            "password",
            "last_login",
            "is_superuser",
        )
