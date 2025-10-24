from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from materials.models import Course, Lesson
from users.models import Subscription
from config.settings import EMAIL_HOST_USER

User = get_user_model()


@shared_task
def send_course_update_notification(course_id, updated_lesson_id=None):
    """
    Асинхронная отправка уведомлений подписанным пользователям об обновлении курса
    """
    course = Course.objects.get(id=course_id)
    updated_lesson = Lesson.objects.get(id=updated_lesson_id) if updated_lesson_id else None

    subscriptions = Subscription.objects.filter(course=course, is_active=True)

    for subscription in subscriptions:
        send_course_update_email.delay(
            user_id=subscription.user.id,
            course_id=course.id,
            lesson_id=updated_lesson.id if updated_lesson else None
        )

    return f"Sent notifications to {subscriptions.count()} subscribers"


@shared_task
def send_course_update_email(user_id, course_id, lesson_id=None):
    """
    Отправка email конкретному пользователю
    """
    user = User.objects.get(id=user_id)
    course = Course.objects.get(id=course_id)
    lesson = Lesson.objects.get(id=lesson_id) if lesson_id else None

    subject = f'Обновление курса: {course.name}'

    if lesson:
        message = f'''
            Здравствуйте, {user.first_name or user.username}!

            В курсе "{course.name}" был обновлен урок "{lesson.name}".
            '''
    else:
        message = f'''
            Здравствуйте, {user.first_name or user.username}!

            Курс "{course.name}" был обновлен.
            '''

    send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )

    return f"Email sent to {user.email}"