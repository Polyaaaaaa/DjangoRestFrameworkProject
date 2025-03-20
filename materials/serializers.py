from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import LinkValidator


class LessonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["user", "course"]


class CourseSerializers(serializers.ModelSerializer):
    lessons = LessonSerializers(
        many=True, read_only=True
    )  # Используем related_name="lessons"
    lesson_quantity = serializers.SerializerMethodField(
        source="lessons.all.first.lessons", read_only=True
    )
    is_subscription = serializers.SerializerMethodField()
    usd_price = serializers.SerializerMethodField

    class Meta:
        model = Course
        fields = "__all__"
        validators = [
            LinkValidator(field="video_link"),
            serializers.UniqueTogetherValidator(
                fields=["name", "description", "video_link"],
                queryset=Course.objects.all(),
            ),
        ]

    def get_lesson_quantity(self, obj):
        return obj.lessons.count()  # Используем related_name="lessons"

    def get_usd_price(self, instance):
        return convert_currencies(instance.amount)
