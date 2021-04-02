import random

from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from communities.models import Community
from subscriptions.models import Subscription


class Command(BaseCommand):
    help = "This Command creates user"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, help="How many user you want to create"
        )

    def handle(self, *args, **options):
        number = int(options.get("number"))
        users = get_user_model().objects.all()
        communities = Community.objects.all()
        c = 0
        for _ in range(number):
            user = random.choice(users)
            community = random.choice(communities)
            try:
                Subscription.objects.create(subscriber=user, community=community)
            except IntegrityError:
                continue
            c += 1
        self.stdout.write(self.style.SUCCESS(f"{c} subscriptions created!"))
