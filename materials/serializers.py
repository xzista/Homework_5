from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lessons_count_in_course = SerializerMethodField()

    def get_lessons_count_in_course(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ('name', 'description', 'lessons_count_in_course',)


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
