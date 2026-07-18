from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from .validators import (
    validate_habit_time,
    validate_periodicity,
    validate_related_habit_and_reward,
    validate_pleasant_habit,
)


class Habit(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )
    place = models.CharField(max_length=255, verbose_name='Место')
    time = models.TimeField(verbose_name='Время выполнения')
    action = models.CharField(max_length=255, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Приятная привычка')
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Связанная привычка',
        related_name='related_to'
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name='Периодичность (дней)',
        help_text='Периодичность выполнения в днях (1-7)'
    )
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name='Вознаграждение')
    duration = models.PositiveIntegerField(
        verbose_name='Время на выполнение (сек)',
        help_text='Не более 120 секунд'
    )
    is_public = models.BooleanField(default=False, verbose_name='Публичная')

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-id']

    def __str__(self):
        return f"{self.action} в {self.time}"

    def clean(self):
        validate_related_habit_and_reward(self)
        validate_pleasant_habit(self)
        validate_habit_time(self.duration)
        validate_periodicity(self.periodicity)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)