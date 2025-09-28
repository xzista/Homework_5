from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import User, Payment


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(ModelSerializer):
    payments = SerializerMethodField()

    def get_payments(self, user):
        payments = user.payments.all()
        return PaymentSerializer(payments, many=True).data

    class Meta:
        model = User
        exclude = ("password", "last_login", "is_superuser",)
