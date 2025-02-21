from rest_framework import serializers

from materials.models import Course, Lesson, Payments


class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class PaymentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
