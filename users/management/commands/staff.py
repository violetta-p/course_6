from django.core.management import BaseCommand
from django.contrib.auth.models import Group
from users.models import User
import os

new_group, created = Group.objects.get_or_create(name='new_group')
# Code to add permission to group ???
ct = ContentType.objects.get_for_model(Project)

# Now what - Say I want to add 'Can add project' permission to new_group?
permission = Permission.objects.create(codename='can_add_project',
                                   name='Can add project',
                                   content_type=ct)
new_group.permissions.add(permission)
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
        my_group = Group.objects.get(name='managers')
        my_group.user_set.add(user)
        user.save()
