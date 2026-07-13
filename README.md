# Habit Tracker

API для трекера полезных привычек с интеграцией Telegram-бота.

## Установка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение: `python -m venv venv`
3. Активируйте: `venv\Scripts\activate` (Windows)
4. Установите зависимости: `pip install -r requirements.txt`
5. Создайте файл `.env` по образцу `.env.template`
6. Выполните миграции: `python manage.py migrate`
7. Создайте суперпользователя: `python manage.py createsuperuser`
8. Запустите сервер: `python manage.py runserver`

## Запуск Celery

- Worker: `celery -A config worker --pool=solo --loglevel=info`
- Beat: `celery -A config beat --loglevel=info`