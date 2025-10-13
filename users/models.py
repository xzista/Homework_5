from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(
        max_length=35, verbose_name="Телефон", blank=True, null=True, help_text="Введите номер телефона"
    )
    city = models.CharField(max_length=35, verbose_name="Город", blank=True, null=True, help_text="Укажите свой город")
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True, help_text="Загрузите свой аватар")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_METHODS = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    PAYMENT_STATUSES = [
        ("pending", "Ожидание"),
        ("paid", "Оплачено"),
        ("failed", "Неудача"),
        ("canceled", "Отменено"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Оплативший пользователь",
        help_text="Укажите плательщика",
        related_name="payments",
    )
    date = models.DateTimeField(verbose_name="Дата проведения оплаты", auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    paid_object = GenericForeignKey("content_type", "object_id")

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, verbose_name="Способ оплаты")

    stripe_session_id = models.CharField(
        max_length=255,
        verbose_name="ID сессии Stripe",
        help_text="Укажите ID сессии Stripe",
        blank=True,
        null=True
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUSES,
        default="pending",
        verbose_name="Статус платежа"
    )
    payment_link = models.URLField(
        max_length=500,
        verbose_name="Ссылка для оплаты",
        help_text="Укажите ссылку на оплату",
        blank=True,
        null=True
    )
    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return f"Оплата {self.paid_object} пользователем {self.user}"


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Подписавшейся пользователь",
        help_text="Укажите пользователя",
        related_name="subscriptions",
    )
    course = models.ForeignKey(
        "materials.Course",
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Подписка на курс",
        related_name="subscriptions",
    )
    is_active = models.BooleanField(
        default=True, verbose_name="Активная подписка", help_text="Отметьте, если подписка активна"
    )
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        status = "активна" if self.is_active else "неактивна"
        return f"Подписка пользователя {self.user} на курс {self.course} - {status}"
