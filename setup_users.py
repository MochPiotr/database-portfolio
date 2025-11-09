import os
import django

# 👇 Ustaw odpowiedni moduł ustawień
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CRM.settings")

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

admin_password = os.environ.get("SUPERUSER_PASSWORD")
carlos_password = os.environ.get("CARLOS_PASSWORD")

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", admin_password)
    print("✅ Stworzono użytkownika admin")
else:
    print("ℹ️ Admin już istnieje")

if not User.objects.filter(username="carlos").exists():
    User.objects.create_user("carlos", "carlos@example.com", carlos_password)
    print("✅ Stworzono użytkownika carlos")
else:
    print("ℹ️ Carlos już istnieje")
