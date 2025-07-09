from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates the first admin user if not exists.'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        if not User.objects.filter(username='dba').exists():
            User.objects.create_superuser(
                username='dba',
                email='dba@example.com',
                password='dba123',
                role='dba'
            )
            self.stdout.write(self.style.SUCCESS("✅ Admin user created."))
        else:
            self.stdout.write(self.style.WARNING("⚠️ Admin user already exists."))
