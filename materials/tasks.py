from datetime import timedelta

from celery import shared_task, Celery
from celery.schedules import crontab
from django.utils.timezone import now
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from materials.models import Course, Lesson, Subscription

User = get_user_model()

app = Celery("config")

app.conf.beat_schedule = {
    "block-inactive-users": {
        "task": "materials.tasks.block_inactive_users",
        "schedule": crontab(hour=0, minute=0),  # Запускаем раз в день
    },
}


@shared_task
def update_send_email(pk, model):
    """Асинхронная отправка уведомлений подписчикам о новых материалах."""
    if model == "Course":
        instance = Course.objects.filter(pk=pk).first()
    else:
        instance = Lesson.objects.filter(pk=pk).first()

    if not instance:
        return "Объект не найден"

    subscribers = instance.subscriptions.all()
    recipient_list = [sub.user.email for sub in subscribers if sub.user.email]

    if recipient_list:
        send_mail(
            subject=f"Обновление в {model}: {instance.name}",
            message=f"Новые материалы в {instance.name}. Проверьте сайт!",
            from_email="noreply@example.com",
            recipient_list=recipient_list,
            fail_silently=True,
        )

    return f"Отправлено {len(recipient_list)} email."


@shared_task
def block_inactive_users():
    """Блокировка пользователей, которые не заходили более месяца."""
    one_month_ago = now() - timedelta(days=30)
    users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    count = users.update(is_active=False)
    return f"Заблокировано {count} пользователей."
