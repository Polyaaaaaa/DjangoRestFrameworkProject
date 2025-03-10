from django.core.management.base import BaseCommand
from materials.models import Course, Lesson
from users.models import User, Payments


class Command(BaseCommand):
    help = "Загружает тестовые платежи в базу данных"

    def handle(self, *args, **kwargs):
        user, _ = User.objects.get_or_create(
            email="testuser@example.com", defaults={"username": "testuser"}
        )
        course, _ = Course.objects.get_or_create(
            name="Python для начинающих", defaults={"description": "Изучите Python"}
        )
        lesson, _ = Lesson.objects.get_or_create(
            name="Введение в Python", defaults={"description": "Первый урок по Python"}
        )

        Payments.objects.create(
            user=user,
            paid_course=course,
            paid_lesson=None,
            payment_date=20240225,
            payment_sum=100.00,
            payment_method="card",
        )

        Payments.objects.create(
            user=user,
            paid_course=None,
            paid_lesson=lesson,
            payment_date=20240226,
            payment_sum=50.00,
            payment_method="paypal",
        )

        self.stdout.write(self.style.SUCCESS("Данные о платежах успешно загружены!"))
