import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arena.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if username and password:
    if not User.objects.filter(username=username).exists():
        print("⚡ Creating superuser...")
        User.objects.create_superuser(username=username, email=email, password=password)
    else:
        print("✅ Superuser already exists. Skipping...")
else:
    print("❌ Missing superuser environment variables. No user created.")
