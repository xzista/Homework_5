from datetime import timedelta

from django.utils import timezone


def should_send_notification(course, lesson=None):
    """
    Проверяет, нужно ли отправлять уведомление об обновлении
    (курс не обновлялся более 4 часов)
    """
    if lesson and lesson.course != course:
        return False

    if hasattr(course, "updated_at"):
        time_since_update = timezone.now() - course.updated_at
        return time_since_update > timedelta(hours=4)

    return True
