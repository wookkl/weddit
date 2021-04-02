import requests
import os
import random

from urllib.request import urlopen
from urllib.error import HTTPError
from tempfile import NamedTemporaryFile

from django.core.files import File
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from posts.models import Post


class Command(BaseCommand):
    help = "This Command creates posts"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, help="How many meme post you want to create"
        )

    def handle(self, *args, **options):
        number = int(options.get("number"))
        users = get_user_model().objects.prefetch_related("subscriptions").all()
        c = 0
        for _ in range(number):
            user = random.choice(users)
            if not user.subscriptions.count():
                continue
            subscriptions = user.subscriptions.select_related("community").all()
            communities = [s.community for s in subscriptions]
            community = random.choice(communities)

            meme = requests.get("https://meme-api.herokuapp.com/gimme").json()
            title = meme.get("title")
            url = meme.get("url")
            ext = os.path.splitext(url)[1]
            postlink = meme.get("postLink")
            if url is None or meme.get("code") == "403":
                continue
            content = f"{title}\n{postlink}"
            img_temp = NamedTemporaryFile(delete=True)
            try:
                img_temp.write(urlopen(url).read())
            except HTTPError:
                continue
            img_temp.flush()

            post = Post.objects.create(
                content=content,
                writer=user,
                community=community,
            )
            post.photo.save(
                f"image_{post.pk}{ext}",
                File(img_temp),
            )
            post.save()
            c += 1

        self.stdout.write(self.style.SUCCESS(f"{c} posts created!"))
