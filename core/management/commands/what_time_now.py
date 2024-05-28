from typing import Any

from django.core.management import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "Displays current time"

    def handle(self, *args: Any, **options: Any) -> str | None:
        time = timezone.now().strftime("%X")
        self.stdout.write("It's now %s." % time)
