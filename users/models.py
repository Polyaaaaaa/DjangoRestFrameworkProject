from django.db import models
from rest_framework import serializers

# Create your models here.
from django.contrib.auth.models import AbstractUser


def get_course_model():
    from materials.models import Course

    return Course


def get_lesson_model():
    from materials.models import Lesson

    return Lesson


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payments(models.Model):
    PAYMENT_METHODS = [
        ("card", "Credit/Debit Card"),
        ("paypal", "PayPal"),
        ("bank", "Bank Transfer"),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
    )
    payment_date = models.PositiveIntegerField(verbose_name="дата платежа")
    paid_course = models.ForeignKey(
        "materials.Course", on_delete=models.CASCADE, null=True, blank=True
    )
    paid_lesson = models.ForeignKey(
        "materials.Lesson", on_delete=models.CASCADE, null=True, blank=True
    )
    payment_sum = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма платежа", help_text="Укажите сумму платежа"
    )
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHODS, verbose_name="Метод оплаты"
    )
    session_id = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="id сессии"
    )
    link = models.URLField(
        max_length=400, null=True, blank=True, verbose_name="ссылка на оплату"
    )

    def __str__(self):
        return f"{self.paid_course if self.paid_course else self.paid_lesson}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ("-payment_date",)
