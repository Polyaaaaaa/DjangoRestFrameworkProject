from django.db import models
from rest_framework import serializers

from config import settings
from materials.validators import NameValidator


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    preview_image = models.ImageField(upload_to='images/', blank=True, null=True)
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural ='курсы'


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", null=True)
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview_image = models.ImageField(upload_to='images/', blank=True, null=True)
    video_link = models.URLField(max_length=200, blank=True, null=True, verbose_name='ссылка на видео')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
