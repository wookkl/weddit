import requests
from urllib.request import urlopen
from tempfile import NamedTemporaryFile

from django.core.files import File
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.core.management.base import BaseCommand
from django_seed import Seed

from communities.models import Community
from .community_list import community_list


class Command(BaseCommand):
    help = "This Command creates communities"

    def handle(self, *args, **options):
        seeder = Seed.seeder()
        for community_name in community_list:
            res = requests.get("https://meme-api.herokuapp.com/gimme").json()
            photo_url = res.get("url")
            if photo_url is None or res.get("code") == "403":
                continue
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(photo_url).read())
            img_temp.flush()

            community = Community.objects.create(
                name=community_name,
                creater=get_user_model().objects.get(nickname="admin"),
                description=seeder.faker.text(),
            )

            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(photo_url).read())
            img_temp.flush()

            community.photo.save("image_%s" % community.pk, File(img_temp))
            community.save()
