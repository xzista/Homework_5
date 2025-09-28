from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer, PaymentFilter


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ["date"]
    ordering = ["-date"]

    def get_serializer_class(self):
        # if self.action == 'retrieve':
        #     return PaymentDetailSerializer
        return PaymentSerializer
