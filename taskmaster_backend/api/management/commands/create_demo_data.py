from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from api.models import Task

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with a demo user and initial tasks'

    def handle(self, *args, **options):
        # Create Demo User
        user, created = User.objects.get_or_create(
            email='demo@taskmaster.com'
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Successfully created demo user (demo@taskmaster.com).'))
        else:
            self.stdout.write(self.style.WARNING('Demo user already exists.'))

        # Create Sample Tasks
        if Task.objects.filter(user=user).exists():
            self.stdout.write(self.style.WARNING('Tasks for demo user already exist. Skipping seed.'))
            return

        tasks_data = [
            {
                'title': 'Complete iOS app integration',
                'description': 'Ensure all network calls map to the new Django REST API perfectly.',
                'priority': 'urgent',
                'category_id': '1',
                'is_completed': False,
                'due_date': timezone.now() + timedelta(days=2)
            },
            {
                'title': 'Design new UI components',
                'description': 'Create Figma designs for the analytics dashboard.',
                'priority': 'high',
                'category_id': '2',
                'is_completed': False,
                'due_date': timezone.now() + timedelta(days=5)
            },
            {
                'title': 'Buy groceries',
                'description': 'Milk, eggs, bread, and coffee beans.',
                'priority': 'medium',
                'category_id': '3',
                'is_completed': False,
                'due_date': timezone.now() + timedelta(days=1)
            },
            {
                'title': 'Pay electricity bill',
                'description': '',
                'priority': 'high',
                'category_id': '3',
                'is_completed': True,
                'due_date': timezone.now() - timedelta(days=1)
            },
            {
                'title': 'Schedule team sync',
                'description': 'Discuss Q2 roadmap and initial feature set.',
                'priority': 'low',
                'category_id': '1',
                'is_completed': False,
                'due_date': timezone.now() + timedelta(days=7)
            }
        ]

        tasks = [Task(user=user, **data) for data in tasks_data]
        Task.objects.bulk_create(tasks)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(tasks)} tasks for the demo user.'))
