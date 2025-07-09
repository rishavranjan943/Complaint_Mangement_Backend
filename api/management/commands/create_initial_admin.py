from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates the first admin user if not exists.'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
                # role='admin' is set by your manager automatically ✅
            )
            self.stdout.write(self.style.SUCCESS("✅ Admin user created."))
        else:
            self.stdout.write(self.style.WARNING("⚠️ Admin user already exists."))
