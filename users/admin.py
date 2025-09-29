from django.contrib import admin

from users.models import Payment, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "phone",
        "city",
        "avatar",
        "is_active",
    )
    list_filter = (
        "email",
        "city",
        "is_active",
    )
    search_fields = (
        "email",
        "city",
        "phone",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "date",
        "content_type",
        "object_id",
        "paid_object",
        "amount",
        "payment_method",
    )
    list_filter = (
        "user",
        "amount",
        "payment_method",
    )
    search_fields = ("user",)
