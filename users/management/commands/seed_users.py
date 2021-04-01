import os
import requests
from urllib.request import urlopen
from urllib.error import HTTPError
from tempfile import NamedTemporaryFile

from django.db.utils import IntegrityError
from django.core.files import File
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from faker import Faker

from posts.models import Post
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
        fake = Faker()
        number_of_communities = Community.objects.all()
        for _ in range(number):
            email = fake.email()
            nickname = fake.first_name()
            password = fake.password(length=10, special_chars=False, upper_case=False)
            if get_user_model().objects.filter(email=email).exists():
                continue
            if get_user_model().objects.filter(nickname=nickname).exists():
                continue
            try:
                user = get_user_model().objects.create_user(
                    email=email,
                    nickname=nickname,
                    password=password,
                )
            except IntegrityError:
                continue
            subscribed_communities = []
            for _ in range(fake.random_int(5, 15)):
                community = number_of_communities[
                    fake.random_int(0, len(number_of_communities) - 1)
                ]
                if not Subscription.objects.filter(
                    community=community, subscriber=user
                ).exists():
                    subscription = Subscription.objects.create(
                        community=community, subscriber=user
                    )
                    subscribed_communities.append(subscription.community)
            for _ in range(fake.random_int(2, 5)):
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
                    community=subscribed_communities[
                        fake.random_int(0, len(subscribed_communities) - 1)
                    ],
                )
                post.photo.save(
                    f"image_{post.pk}{ext}",
                    File(img_temp),
                )
                post.save()
