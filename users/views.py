from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.permissions import UserProfilePermission
from users.serializers import (PaymentFilter, PaymentSerializer,
                               UserPublicSerializer, UserSerializer)
from users.services import create_stripe_session


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer
    permission_classes = (IsAuthenticated,)


class UserRetrieveApiView(RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (UserProfilePermission,)

    def get_serializer_class(self):
        obj = self.get_object()
        if obj == self.request.user:
            return UserSerializer
        return UserPublicSerializer


class UserUpdateApiView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserProfilePermission,)


class UserDestroyApiView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserProfilePermission,)


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

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        session_id, payment_link = create_stripe_session(payment)
        payment.stripe_session_id = session_id
        payment.payment_link = payment_link
        payment.save()