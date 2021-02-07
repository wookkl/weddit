import tempfile

from django.test import TestCase
from django.contrib.auth import get_user_model

from communities.models import Community


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class CommunityModelTests(TestCase):
    """Model test"""

    def setUp(self):
        self.user = create_user(
            **{
                "email": "test@gmail.com",
                "nickname": "test name",
                "password": "password123@",
            }
        )

    def test_create_new_community_success(self):
        """Test creating a new community success"""
        creater = self.user
        name = "testTitle"
        description = "this is test community"
        avatar = tempfile.NamedTemporaryFile(suffix=".jpg").name
        photo = tempfile.NamedTemporaryFile(suffix=".png").name

        community = Community.objects.create(
            creater=creater,
            name=name,
            description=description,
            avatar=avatar,
            photo=photo,
        )

        self.assertEqual(community.creater, creater)
        self.assertEqual(1, Community.objects.all().count())
        self.assertEqual(str(community), name)
