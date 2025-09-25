from django.contrib.auth.models import AbstractUser
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
