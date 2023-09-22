from django.core.management import BaseCommand
from users.models import User
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=os.getenv('EMAIL_HOST_ADMIN'),
            first_name='Admin',
            last_name='Admin',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        user.set_password(os.getenv('DJANGO_ADMIN_PW'))
        user.save()
