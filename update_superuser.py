import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lhs_project.settings')
django.setup()

from authentication.models import User

# Update the superuser's role
user = User.objects.get(username='hiteshy44')
user.role = User.Role.SUPERADMIN
user.save()

print(f"Updated {user.username}'s role to {user.role}") 