from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from faker import Faker


class Command(BaseCommand):
    help = "This Command creates user"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, help="How many user you want to create"
        )

    def handle(self, *args, **options):
        number = int(options.get("number"))
        fake = Faker()
        c = 0

        for _ in range(number):
            email = fake.email()
            nickname = fake.first_name()
            password = fake.password(length=10, special_chars=False, upper_case=False)

            try:
                get_user_model().objects.create_user(
                    email=email,
                    nickname=nickname,
                    password=password,
                )
            except IntegrityError:
                continue

            c += 1

        self.stdout.write(self.style.SUCCESS(f"{c} users created!"))
