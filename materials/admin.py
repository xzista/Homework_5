from django.contrib import admin

from materials.models import Course, Lesson


@admin.register(Course)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "owner",
        "price",
        "preview_image",
    )
    list_filter = (
        "owner",
    )
    search_fields = ("name", "description",)

@admin.register(Lesson)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "course",
        "url_video",
        "owner",
        "price",
        "preview_image",
    )
    list_filter = (
        "owner",
        "course",
    )
    search_fields = ("name", "description",)

