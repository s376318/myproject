"""
Django management command to initialize the application with sample data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from vlogapp.models import Category, VlogPost
from datetime import timedelta


class Command(BaseCommand):
    help = 'Initializes the vlog application with sample categories and vlogs'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Reset database before adding sample data')

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Deleting existing data...')
            VlogPost.objects.all().delete()
            Category.objects.all().delete()
            User.objects.filter(username='admin').delete()

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('✓ Superuser created: admin / admin123'))

        # Create sample user
        if not User.objects.filter(username='creator').exists():
            User.objects.create_user('creator', 'creator@example.com', 'creator123')
            self.stdout.write(self.style.SUCCESS('✓ User created: creator / creator123'))

        # Create categories
        categories_data = [
            {'name': 'Django Tutorials', 'description': 'Learn Django web development'},
            {'name': 'Python Basics', 'description': 'Python programming fundamentals'},
            {'name': 'Web Development', 'description': 'Web development tips and tricks'},
            {'name': 'Technology News', 'description': 'Latest tech news and updates'},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Category created: {cat.name}'))

        # Get users
        admin_user = User.objects.get(username='admin')
        creator_user = User.objects.get(username='creator')

        # Create sample vlogs
        vlogs_data = [
            {
                'title': 'Getting Started with Django',
                'description': 'Learn the basics of Django framework including models, views, and templates.',
                'video_url': 'https://www.youtube.com/watch?v=rHux0gMZ3Eg',
                'category': 'Django Tutorials',
                'author': admin_user,
                'tags': 'django, python, tutorial, beginner',
                'days_ago': 5
            },
            {
                'title': 'Python List Comprehensions Explained',
                'description': 'Master Python list comprehensions with practical examples and use cases.',
                'video_url': 'https://www.youtube.com/watch?v=DxCJBeF2MqE',
                'category': 'Python Basics',
                'author': creator_user,
                'tags': 'python, list comprehension, tutorial',
                'days_ago': 3
            },
            {
                'title': 'Responsive Web Design with Bootstrap',
                'description': 'Create beautiful responsive websites using Bootstrap CSS framework.',
                'video_url': 'https://www.youtube.com/watch?v=ZxoDjaCHiBo',
                'category': 'Web Development',
                'author': admin_user,
                'tags': 'bootstrap, css, responsive, web design',
                'days_ago': 2
            },
            {
                'title': 'Latest AI Technology Trends 2024',
                'description': 'Discover the latest trends in artificial intelligence and machine learning.',
                'video_url': 'https://www.youtube.com/watch?v=kCc8FmEb1nY',
                'category': 'Technology News',
                'author': creator_user,
                'tags': 'ai, machine learning, technology, news',
                'days_ago': 1
            },
        ]

        for vlog_data in vlogs_data:
            vlog, created = VlogPost.objects.get_or_create(
                title=vlog_data['title'],
                defaults={
                    'description': vlog_data['description'],
                    'video_url': vlog_data['video_url'],
                    'category': categories[vlog_data['category']],
                    'author': vlog_data['author'],
                    'tags': vlog_data['tags'],
                    'published_date': timezone.now() - timedelta(days=vlog_data['days_ago']),
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Vlog created: {vlog.title}'))

        self.stdout.write(self.style.SUCCESS('\n✓ Initialization complete!'))
        self.stdout.write('\nAdmin URL: http://localhost:8000/admin/')
        self.stdout.write('Username: admin')
        self.stdout.write('Password: admin123')
