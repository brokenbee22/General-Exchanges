import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Creates or updates an admin user from Render environment variables."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.getenv("ADMIN_USERNAME")
        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")

        if not username or not email or not password:
            self.stdout.write("Admin env vars are missing. Skipping admin setup.")
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email}
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS("Admin user created."))
        else:
            self.stdout.write(self.style.SUCCESS("Admin user updated."))