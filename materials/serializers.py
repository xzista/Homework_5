from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lessons_count_in_course = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count_in_course(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = (
            "name",
            "description",
            "lessons_count_in_course",
            "lessons",
        )
