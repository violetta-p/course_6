from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from users.models import User
import os

new_group, created = Group.objects.get_or_create(name='managers')
ct = ContentType.objects.get_for_model(User)

permission = Permission.objects.create(codename='can_add_project',
                                   name='Can view Category',
                                   content_type=ct)
new_group.permissions.add(permission)