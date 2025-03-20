from django.db import models
from config import settings

User = settings.AUTH_USER_MODEL


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название")
    preview_image = models.ImageField(upload_to="images/", blank=True, null=True)
    description = models.TextField(verbose_name="Описание")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="courses"
    )
    amount = models.IntegerField(default=1000, verbose_name="Цена")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")  # Новое поле

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name"]


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", null=True
    )
    name = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    preview_image = models.ImageField(upload_to="images/", blank=True, null=True)
    video_link = models.URLField(
        max_length=200, blank=True, null=True, verbose_name="Ссылка на видео"
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="lessons"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")  # Новое поле

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["name"]


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        null=True,
        blank=True,
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="subscriptions", null=True
    )

    def __str__(self):
        return f"{self.user} подписан на курс {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ("user", "course")  # Запрещает дублирование подписок
        ordering = ["user"]
