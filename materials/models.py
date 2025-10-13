from django.conf import settings
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название курса", help_text="Укажите название курса")
    description = models.TextField(verbose_name="Описание", help_text="Введите описание курса", blank=True, null=True)
    preview_image = models.ImageField(
        upload_to="materials/course_preview_image/", blank=True, null=True, help_text="Загрузите превью курса"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца курса",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Стоимость курса",
        help_text="Укажите стоимость курса в рублях"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название урока", help_text="Укажите название урока")
    description = models.TextField(verbose_name="Описание", help_text="Введите описание урока", blank=True, null=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс урока",
        help_text="Выберите к какому курсу относится урок",
        related_name="lessons",
    )
    preview_image = models.ImageField(
        upload_to="materials/lesson_preview_image/", blank=True, null=True, help_text="Загрузите превью урока"
    )
    url_video = models.CharField(
        max_length=100, verbose_name="Ссылка на видео урока", help_text="Укажите ссылку на видео урока"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца урока",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Стоимость урока",
        help_text="Укажите стоимость урока в рублях"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name
