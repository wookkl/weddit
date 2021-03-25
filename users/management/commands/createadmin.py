from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = "This Command creates admin"

    def handle(self, *args, **options):
        get_user_model().objects.create_superuser(
            email=os.environ.get("ADMIN_EMAIL"),
            nickname="admin",
            password=os.environ.get("ADMIN_PASSWORD"),
        )
