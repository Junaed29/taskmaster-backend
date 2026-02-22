from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskMasterTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password123')
        self.other_user = User.objects.create_user(email='other@example.com', password='password123')
        self.task = Task.objects.create(
            user=self.user,
            title='My Task',
            description='Test Description',
            priority='high',
            category_id='1'
        )
        self.other_task = Task.objects.create(
            user=self.other_user,
            title='Other Task',
            priority='low'
        )
        self.login_url = reverse('token_obtain_pair')
        self.tasks_url = reverse('task-list')

    def authenticate(self):
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user_id', response.data)
        self.assertEqual(response.data['user_id'], self.user.id)

    def test_get_tasks_unauthenticated(self):
        response = self.client.get(self.tasks_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_tasks_authenticated_and_isolated(self):
        self.authenticate()
        response = self.client.get(self.tasks_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only return one task (from self.user)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'My Task')

    def test_create_task(self):
        self.authenticate()
        data = {
            'title': 'New API Task',
            'description': 'DRF integration',
            'priority': 'urgent',
            'category_id': '2',
            'due_date': '2026-03-01T10:00:00Z'
        }
        response = self.client.post(self.tasks_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(Task.objects.get(title='New API Task').user, self.user)

    def test_toggle_task(self):
        self.authenticate()
        toggle_url = reverse('task-toggle', kwargs={'pk': self.task.id})
        
        # Turn it on
        response = self.client.patch(toggle_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_completed'], True)
        
        # Turn it off
        response = self.client.patch(toggle_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_completed'], False)
