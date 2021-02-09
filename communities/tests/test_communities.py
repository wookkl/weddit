import tempfile

from django.test import TestCase, Client
from django.urls import reverse
from django.core.validators import ValidationError
from django.conf import settings


from communities.models import Community
from core.tests.sample_objects import get_sample_user, get_sample_community

COMMUNITY_LIST_URL = reverse("communities:list")
COMMUNITY_CREATE_URL = reverse("communities:create")


class CommunityModelTests(TestCase):
    """Model test"""

    def setUp(self):
        self.user = get_sample_user()

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
        self.user = get_sample_user()
        self.client.force_login(self.user)

    def test_retrieve_communities(self):
        """Test retrieving a list of communities"""

        get_sample_community(creater=self.user)
        get_sample_community(creater=self.user, **{"name": "test2"})
        res = self.client.get(COMMUNITY_LIST_URL)
        communities = Community.objects.all().order_by("-id")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(2, communities.count())

    def test_create_new_community_success(self):
        payload = {
            "creater": self.user,
            "name": "testname",
            "description": "test description",
        }
        res = self.client.post(COMMUNITY_CREATE_URL, payload)
        community = Community.objects.get(name=payload["name"])

        self.assertRedirects(res, community.get_absolute_url())
        self.assertTrue(Community.objects.filter(name=payload["name"]).exists())
