from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django_seed import Seed

from communities.models import Community

from .community_list import community_list


class Command(BaseCommand):
    help = "This Command creates communities"

    def handle(self, *args, **options):
        seeder = Seed.seeder()
        for community_name in community_list:
            community = Community.objects.create(
                name=community_name,
                creater=get_user_model().objects.get(nickname="admin"),
                description=seeder.faker.text(),
            )
            community.save()
