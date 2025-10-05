from django.db import models

from users.models import User


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название курса", help_text="Укажите название курса")
    description = models.TextField(verbose_name="Описание", help_text="Введите описание курса", blank=True, null=True)
    preview_image = models.ImageField(
        upload_to="materials/course_preview_image/", blank=True, null=True, help_text="Загрузите превью курса"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца курса",
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
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца урока",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name
