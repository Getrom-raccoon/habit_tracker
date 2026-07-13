from django.core.exceptions import ValidationError


def validate_habit_time(value):
    """Время выполнения не должно превышать 120 секунд"""
    if value > 120:
        raise ValidationError('Время выполнения не может превышать 120 секунд')


def validate_periodicity(value):
    """Периодичность должна быть от 1 до 7 дней"""
    if value < 1 or value > 7:
        raise ValidationError('Периодичность должна быть от 1 до 7 дней')


def validate_related_habit_and_reward(habit):
    """Нельзя одновременно заполнять related_habit и reward"""
    if habit.related_habit and habit.reward:
        raise ValidationError('Нельзя одновременно указать связанную привычку и вознаграждение')

    if habit.related_habit and not habit.related_habit.is_pleasant:
        raise ValidationError('Связанная привычка должна быть приятной')


def validate_pleasant_habit(habit):
    """У приятной привычки не может быть вознаграждения или связанной привычки"""
    if habit.is_pleasant:
        if habit.reward:
            raise ValidationError('У приятной привычки не может быть вознаграждения')
        if habit.related_habit:
            raise ValidationError('У приятной привычки не может быть связанной привычки')