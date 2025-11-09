import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

admin_password = os.environ.get("SUPERUSER_PASSWORD")
carlos_password = os.environ.get("CARLOS_PASSWORD")

admin_user = User.objects.filter(username="admin").first()
if admin_user:
    admin_user.set_password(admin_password)
    admin_user.save()
    print("Superuser admin: hasło zaktualizowane")
else:
    User.objects.create_superuser("admin", "admin@example.com", admin_password)
    print("Superuser admin: utworzony")

if not User.objects.filter(username="carlos").exists():
    User.objects.create_user("carlos", "carlos@example.com", carlos_password)
    print("Użytkownik carlos: utworzony")
else:
    print("Użytkownik carlos: już istnieje")
