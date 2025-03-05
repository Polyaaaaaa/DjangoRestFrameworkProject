from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import NameValidator


class LessonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializers(serializers.ModelSerializer):
    lessons = LessonSerializers(many=True, read_only=True)  # Используем related_name="lessons"
    lesson_quantity = serializers.SerializerMethodField(source='lessons.all.first.lessons')

    class Meta:
        model = Course
        fields = '__all__'
        validators = [
            NameValidator(field='name'),
            serializers.UniqueTogetherValidator(fields=['name', 'description'], queryset=Course.objects.all())
        ]

    def get_lesson_quantity(self, obj):
        return obj.lessons.count()  # Используем related_name="lessons"
