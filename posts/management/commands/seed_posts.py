import random
import requests
from urllib.request import urlopen
from tempfile import NamedTemporaryFile

from django.core.files import File
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.core.management.base import BaseCommand
from django_seed import Seed

from posts.models import Post
from communities.models import Community


class Command(BaseCommand):
    help = "This Command creates posts"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, help="How many meme post you want to create"
        )

    def handle(self, *args, **options):
        number = int(options.get("number"))
        number_of_communities = Community.objects.count()
        for _ in range(number):
            meme = requests.get("https://meme-api.herokuapp.com/gimme").json()
            title = meme.get("title")
            url = meme.get("url")
            postlink = meme.get("postLink")
            if url is None or meme.get("code") == "403":
                continue
            content = f"{title}  출처:{postlink}"
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(url).read())
            img_temp.flush()

            post = Post.objects.create(
                content=content,
                writer=get_user_model().objects.get(nickname="admin"),
                community=Community.objects.get(
                    pk=random.randint(1, number_of_communities)
                ),
            )
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(url).read())
            img_temp.flush()

            post.photo.save("image_%s" % post.pk, File(img_temp))
            post.save()
