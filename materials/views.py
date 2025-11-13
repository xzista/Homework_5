from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.paginators import CustomPagination
from materials.serializers import (CourseDetailSerializer, CourseSerializer,
                                   LessonSerializer)
from users.models import Subscription
from users.permissions import IsModer, IsNotModer, IsOwner
from users.tasks import send_course_update_notification
from users.utils import should_send_notification


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()

    def get_pagination_class(self):
        if self.action == "list":
            return CustomPagination
        return None

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        """Обновление курса с отправкой уведомлений"""
        instance = serializer.save()

        if should_send_notification(instance):
            send_course_update_notification.delay(instance.id)

    @action(detail=True, methods=["post"])
    def update_lessons(self, request, pk=None):
        """Массовое обновление уроков курса"""
        course = self.get_object()
        lessons_data = request.data.get("lessons", [])

        updated_lessons = []
        for lesson_data in lessons_data:
            lesson_id = lesson_data.get("id")
            if lesson_id:
                try:
                    lesson = Lesson.objects.get(id=lesson_id, course=course)
                    serializer = LessonSerializer(lesson, data=lesson_data, partial=True)
                    if serializer.is_valid():
                        updated_lesson = serializer.save()
                        updated_lessons.append(updated_lesson.id)
                except Lesson.DoesNotExist:
                    continue

        if updated_lessons and should_send_notification(course):
            for lesson_id in updated_lessons:
                send_course_update_notification.delay(course.id, lesson_id)

        return Response(
            {"message": f"Updated {len(updated_lessons)} lessons", "updated_lessons": updated_lessons},
            status=status.HTTP_200_OK,
        )

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (IsNotModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (
                IsNotModer,
                IsOwner,
            )
        return super().get_permissions()


class LessonsCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        IsNotModer,
    ]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

        print("=== NEW LESSON CREATED ===")
        result = send_course_update_notification.delay(lesson.course.id, lesson.id)
        print(f"=== Task ID for new lesson: {result.id} ===")


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]

    def perform_update(self, serializer):
        """Обновление урока с отправкой уведомлений"""
        instance = serializer.save()

        print("=== LESSON UPDATED VIA LessonUpdateApiView ===")
        print(f"Lesson ID: {instance.id}")
        print(f"Course ID: {instance.course.id}")

        if should_send_notification(instance.course, instance):
            print("=== SENDING NOTIFICATION ===")
            result = send_course_update_notification.delay(instance.course.id, instance.id)
            print(f"=== Task ID: {result.id} ===")
        else:
            print("=== NOTIFICATION NOT NEEDED (updated recently) ===")


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModer, IsOwner]


class SubscriptionAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})
