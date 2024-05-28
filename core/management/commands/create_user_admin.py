import getpass
import re
from typing import Any

from django.core.management.base import BaseCommand, CommandError

from user_authentication.models import Role, UserAccount


class Command(BaseCommand):
    help = "Create admin"

    def handle(self, *args: Any, **options: Any) -> str | None:
        email = input("Enter the email:")
        password = getpass.getpass("Enter your password.")
        repassword = getpass.getpass("Enter your password again.")
        phone = input("Enter phone number.")
        if len(password) < 5:
            raise CommandError("Error: Password must be at least 8 characters long.")

        if password != repassword:
            raise CommandError("Error: Passwords don't match.")

        pattern = r"^9[0-9]{9}$"
        match = re.match(pattern, phone)
        if match is None:
            raise CommandError({"phone": "Enter a valid phone number"})

        try:
            UserAccount.objects.create(
                email=email, password=password, role=Role.A, phone_number=phone
            )
            self.stdout.write(f"Admin created")
        except Exception as e:
            self.stdout.write(f"Error creating admin user: {e}")
