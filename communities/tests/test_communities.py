import tempfile

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.validators import ValidationError
from django.conf import settings

from communities.models import Community

COMMUNITY_LIST_URL = reverse("communities:list")
COMMUNITY_CREATE_URL = reverse("communities:create")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def sample_community(creater, **params):
    defaults = {
        "creater": creater,
        "name": "testTitle",
        "description": "this is test community",
        "avatar": tempfile.NamedTemporaryFile(suffix=".jpg").name,
        "photo": tempfile.NamedTemporaryFile(suffix=".png").name,
    }
    defaults.update(params)
    return Community.objects.create(**defaults)


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

    def test_auth_required(self):
        """ Test that authentication is required """
        payload = {
            "name": "testname",
            "description": "test description",
        }

        res = self.client.post(COMMUNITY_CREATE_URL, payload)
        self.assertRedirects(
            res,
            settings.LOGIN_URL + "?next=/communities/create/",
        )


class PrivateCommunityTest(TestCase):
    """Private community test"""

    def setUp(self):
        self.client = Client()
        self.user = create_user(
            **{
                "email": "test@gmail.com",
                "nickname": "testname",
                "password": "password123@",
            }
        )

    def test_retrieve_communities(self):
        """Test retrieving a list of communities"""
        sample_community(creater=self.user)
        sample_community(creater=self.user, **{"name": "test2"})

        res = self.client.get(COMMUNITY_LIST_URL)
        communities = Community.objects.all().order_by("-id")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(2, communities.count())

    # def test_create_new_community_success(self):
    #     payload = {
    #         "name": "testname",
    #         "description": "test description",
    #     }
    #     res = self.client.post(COMMUNITY_LIST_URL, payload)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(Community.objects.filter(name=payload["name"]).exists())