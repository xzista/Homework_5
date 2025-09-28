from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register("user", UserViewSet)
router.register("payments", PaymentViewSet)

urlpatterns = []

urlpatterns += router.urls
