import tempfile

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.validators import ValidationError

from communities.models import Community


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class CommunityModelTests(TestCase):
    """Model test"""

    def setUp(self):
        self.user = create_user(
            **{
                "email": "test@gmail.com",
                "nickname": "testname",
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

    def test_create_new_community_invalid_field(self):
        """Test creating a new community with invalid fields"""
        creater = self.user
        name = "space name"
        description = "this is test community"
        avatar = tempfile.NamedTemporaryFile(suffix=".jpg").name
        photo = tempfile.NamedTemporaryFile(suffix=".png").name

        with self.assertRaises(ValidationError):
            Community.objects.create(
                creater=creater,
                name=name,
                description=description,
                avatar=avatar,
                photo=photo,
            )


class PublicCommunityTests(TestCase):
    """Public community test"""

    def setUp(self):
        self.client = Client()
