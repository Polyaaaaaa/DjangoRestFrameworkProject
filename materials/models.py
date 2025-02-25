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
