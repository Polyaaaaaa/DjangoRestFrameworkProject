from rest_framework import serializers

from materials.models import Course, Lesson, Payments


class LessonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializers(serializers.ModelSerializer):
    lesson_quantity = serializers.SerializerMethodField()  # Количество уроков
    lessons = LessonSerializers(many=True, read_only=True, source="lesson_set")  # Информация о всех уроках

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_quantity(self, obj):
        return obj.lesson_set.count()  # Подсчет количества уроков


class PaymentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
