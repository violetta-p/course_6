from django.core.management import BaseCommand
from django.contrib.auth.models import Group
from users.models import User
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=os.getenv('EMAIL_HOST_MANAGER'),
            first_name='Manager',
            last_name='Manager',
            is_superuser=False,
            is_staff=True,
            is_active=True,
        )
        user.set_password(os.getenv('DJANGO_MANAGER_PW'))
        user.save()
