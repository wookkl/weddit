import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from posts.models import Post
from votes.models import Vote


class Command(BaseCommand):
    help = "This Command creates votes"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, help="How many vote you want to create"
        )

    def handle(self, *args, **options):
        number = int(options.get("number"))
        users = get_user_model().objects.all()
        posts = Post.objects.all()
        c = 0
        for _ in range(number):
            user = random.choice(users)
            post = random.choice(posts)
            exists = Vote.objects.filter(voter=user, post=post).exists()
            if exists:
                continue
            Vote.objects.create(
                voter=user, post=post, like=random.choice([True, False])
            )
            c += 1
        self.stdout.write(self.style.SUCCESS(f"{c} votes created!"))
