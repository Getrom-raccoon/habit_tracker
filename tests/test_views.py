from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from habits.models import Habit

User = get_user_model()


class HabitAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@test.com', password='pass123')
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        url = reverse('habit-list')
        data = {
            'place': 'Home',
            'time': '09:00:00',
            'action': 'Read book',
            'duration': 30,
            'periodicity': 1,
            'reward': 'Tea'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)

    def test_list_habits(self):
        Habit.objects.create(
            owner=self.user,
            place='Home',
            time='09:00:00',
            action='Read',
            duration=30,
            periodicity=1
        )
        url = reverse('habit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)