from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from habits.models import Habit

User = get_user_model()


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@test.com', password='test123')

    def test_valid_habit_creation(self):
        habit = Habit.objects.create(
            owner=self.user,
            place='Home',
            time='09:00:00',
            action='Morning exercise',
            is_pleasant=False,
            duration=60,
            periodicity=1,
            reward='Coffee'
        )
        self.assertEqual(habit.action, 'Morning exercise')
        self.assertEqual(habit.duration, 60)

    def test_habit_time_validation(self):
        with self.assertRaises(ValidationError):
            habit = Habit(
                owner=self.user,
                place='Home',
                time='09:00:00',
                action='Test',
                duration=150,  # > 120
                periodicity=1
            )
            habit.full_clean()

    def test_periodicity_validation(self):
        with self.assertRaises(ValidationError):
            habit = Habit(
                owner=self.user,
                place='Home',
                time='09:00:00',
                action='Test',
                duration=60,
                periodicity=8  # > 7
            )
            habit.full_clean()