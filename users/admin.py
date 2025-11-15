from django.contrib import admin

from users.models import Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "phone",
        "city",
        "is_active",
        "get_subscriptions_count",
        "get_active_subscriptions_count",
    )
    list_filter = (
        "is_active",
        "city",
    )
    search_fields = (
        "email",
        "phone",
        "city",
    )

    def get_subscriptions_count(self, obj):
        return obj.subscriptions.count()

    get_subscriptions_count.short_description = "Всего подписок"

    def get_active_subscriptions_count(self, obj):
        return obj.subscriptions.filter(is_active=True).count()

    get_active_subscriptions_count.short_description = "Активных подписок"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "course",
        "is_active",
        "subscribed_at",
    )
    list_filter = (
        "is_active",
        "course",
        "subscribed_at",
    )
    search_fields = (
        "user__email",
        "course__name",
    )
    list_editable = ("is_active",)
