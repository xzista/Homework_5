from rest_framework.fields import SerializerMethodField
from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_video_url


class LessonSerializer(serializers.ModelSerializer):
    url = serializers.CharField(validators=[validate_video_url])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
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
