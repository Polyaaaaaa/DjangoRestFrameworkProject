# from django.shortcuts import render
from django.utils.decorators import method_decorator
from django_celery_beat.utils import now
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import MaterialsPaginator
from materials.permissions import IsOwnerOrStaff
from materials.serializers import (
    CourseSerializers,
    LessonSerializers,
    SubscriptionSerializer,
)

from rest_framework.permissions import IsAuthenticated, AllowAny

from materials.tasks import update_send_email


# Create your views here.
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="description from swagger_auto_schema via method_decorator"
    ),
)
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializers
    queryset = Course.objects.all()
    permission_classes = [AllowAny]


class CourseUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CourseSerializers
    queryset = Course.objects.all()

    def perform_update(self, serializer):
        course = serializer.save()
        last_updated = (
            course.updated_at
        )  # Убедитесь, что в модели Course есть поле `updated_at`

        # Проверяем, прошло ли 4 часа с последнего обновления
        if last_updated is None or (now() - last_updated).total_seconds() > 14400:
            update_send_email.delay(course.pk, "Course")


class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseSerializers
    queryset = Course.objects.all().order_by("name")
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]
    pagination_class = MaterialsPaginator

    def get(self, request, **kwargs):
        queryset = Course.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = CourseSerializers(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializers
    permission_classes = [AllowAny]
    pagination_class = MaterialsPaginator

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all().order_by("name")
    permission_classes = [AllowAny, IsOwnerOrStaff]
    pagination_class = MaterialsPaginator

    def get(self, request, **kwargs):
        queryset = Lesson.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = LessonSerializers(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny, IsOwnerOrStaff]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()

    def perform_update(self, serializer):
        lesson = serializer.save()
        course = lesson.course
        last_updated = course.updated_at  # Поле должно быть в модели Course

        if last_updated is None or (now() - last_updated).total_seconds() > 14400:
            update_send_email.delay(course.pk, "Course")


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny, IsOwnerOrStaff]


class SubscriptionAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = request.user  # Получаем текущего пользователя
        course_id = request.data.get("course_id")  # Получаем ID курса из запроса
        course_item = get_object_or_404(Course, id=course_id)  # Получаем объект курса

        subs_item = Subscription.objects.filter(
            user=user, course=course_item
        )  # Проверяем подписку

        if subs_item.exists():
            subs_item.delete()  # Удаляем подписку
            message = "Подписка удалена"
        else:
            Subscription.objects.create(
                user=user, course=course_item
            )  # Создаем подписку
            message = "Подписка добавлена"

        return Response({"message": message})


# class SubscriptionCreateAPIView(generics.CreateAPIView):
#     serializer_class = SubscriptionSerializer
#
#     def perform_create(self, serializer):
#         new_subscription = serializer.save()
#         if new_subscription.course:
#             send_email.delay(new_subscription.course_id, 'Course')
#         else:
#             send_email.delay(new_subscription.lesson_id, 'Lesson')
