import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django_seed import Seed

from posts.models import Post
from comments.models import Comment


class Command(BaseCommand):
    help = "This Command creates comments"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, help="How many comment you want to create"
        )

    def handle(self, *args, **options):
        number = int(options.get("number"))
        seeder = Seed.seeder()
        posts = Post.objects.all()
        users = get_user_model().objects.all()

        for _ in range(number):
            comment = Comment.objects.create(
                comment=seeder.faker.text(),
                writer=random.choice(users),
                post=random.choice(posts),
            )
            comment.save()

        self.stdout.write(self.style.SUCCESS(f"{number} comments created!"))
