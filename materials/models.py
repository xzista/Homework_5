from django.db import models

class Course(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Название курса", help_text="Укажите название курса"
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание курса", blank=True, null=True
    )
    preview_image = models.ImageField(
        upload_to='materials/preview_image/', blank=True, null=True, help_text='Загрузите превью курса'
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name
