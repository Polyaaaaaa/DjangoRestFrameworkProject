from rest_framework import serializers

from materials.models import Course, Lesson


class LessonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "name", "description", "video_link", "course"]


class CourseSerializers(serializers.ModelSerializer):
    lessons = LessonSerializers(many=True, read_only=True)  # Используем related_name="lessons"
    lesson_quantity = serializers.SerializerMethodField(source='lessons.all.first.lessons')

    class Meta:
        model = Course
        fields = ["id", "name", "description", "lessons", "lesson_quantity"]

    def get_lesson_quantity(self, obj):
        return obj.lessons.count()  # Используем related_name="lessons"
