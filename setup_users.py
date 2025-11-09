import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CRM.settings")
django.setup()

from django.contrib.auth import get_user_model
from leads.models import Agent

User = get_user_model()

admin_password = os.environ.get("SUPERUSER_PASSWORD")
carlos_password = os.environ.get("CARLOS_PASSWORD")

# Tworzenie admina
admin_user, created = User.objects.get_or_create(
    username="admin",
    defaults={
        "email": "admin@example.com",
        "is_superuser": True,
        "is_staff": True,
        "is_organisor": True,
        "is_agent": False,
    },
)
if created:
    admin_user.set_password(admin_password)
    admin_user.save()
    print("✅ Stworzono admina")

# Tworzenie Carlosa
carlos_user, created = User.objects.get_or_create(
    username="carlos",
    defaults={
        "email": "carlos@example.com",
        "is_agent": True,
        "is_organisor": False,
    },
)
if created:
    carlos_user.set_password(carlos_password)
    carlos_user.save()
    print("✅ Stworzono Carlosa")

# Tworzenie agenta dla Carlosa
Agent.objects.get_or_create(user=carlos_user, organisation=carlos_user.userprofile)
print("✅ Carlos przypisany jako Agent")
