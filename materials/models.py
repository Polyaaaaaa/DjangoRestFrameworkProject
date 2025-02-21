from django.db import models
from users.models import User


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    preview_image = models.ImageField(upload_to='images/', blank=True, null=True)
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural ='курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview_image = models.ImageField(upload_to='images/', blank=True, null=True)
    video_link = models.URLField(max_length=200, blank=True, null=True, verbose_name='ссылка на видео')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payments(models.Model):
    PAYMENT_METHODS = [
        ('card', 'Credit/Debit Card'),
        ('paypal', 'PayPal'),
        ('bank', 'Bank Transfer'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', verbose_name="Пользователь")
    payment_date = models.PositiveIntegerField(verbose_name="дата платежа")
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    payment_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма платежа")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, verbose_name="Метод оплаты")

    def __str__(self):
        return f"{self.paid_course if self.paid_course else self.paid_lesson}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ('-payment_date',)
