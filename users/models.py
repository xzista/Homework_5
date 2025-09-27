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
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(User,
        on_delete=models.CASCADE,
        verbose_name="Оплативший пользователь",
        help_text="Укажите плательщика",
        related_name="payments",)
    data = models.DateTimeField(verbose_name="Дата проведения оплаты", auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    paid_object = GenericForeignKey("content_type", "object_id")

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, verbose_name="Способ оплаты")

    def __str__(self):
        return f"Оплата {self.paid_object} пользователем {self.user}"