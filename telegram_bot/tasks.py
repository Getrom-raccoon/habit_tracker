import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from habits.models import Habit
from users.models import User


@shared_task
def send_habit_reminders():
    """Отправка напоминаний о привычках"""
    now = timezone.now().time()
    today = timezone.now().date()

    habits = Habit.objects.filter(
        is_pleasant=False,
        owner__telegram_chat_id__isnull=False
    )

    for habit in habits:
        # Проверка, нужно ли напомнить сегодня
        days_since = (today - habit.created_at.date()).days
        if days_since % habit.periodicity != 0:
            continue

        # Проверка времени (с запасом 5 минут)
        habit_time = habit.time
        time_diff = abs(
            (now.hour * 60 + now.minute) -
            (habit_time.hour * 60 + habit_time.minute)
        )
        if time_diff > 5:
            continue

        user = habit.owner
        if not user.telegram_chat_id:
            continue

        message = f"Напоминание о привычке!\n\n"
        message += f"Действие: {habit.action}\n"
        message += f"Место: {habit.place}\n"
        message += f"Время: {habit.time.strftime('%H:%M')}\n"

        if habit.related_habit:
            message += f"После выполнения вознаградите себя: {habit.related_habit.action}\n"
        elif habit.reward:
            message += f"Вознаграждение: {habit.reward}\n"

        send_telegram_message.delay(user.telegram_chat_id, message)


@shared_task
def send_telegram_message(chat_id, message):
    """Отправка сообщения в Telegram"""
    token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {'error': str(e)}