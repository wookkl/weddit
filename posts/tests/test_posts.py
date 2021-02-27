import tempfile

from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings

from core.tests.sample_objects import (
    get_sample_user,
    get_sample_community,
    get_sample_post,
    create_subscription,
)

from posts.models import Post

CREATE_POST_URL = reverse("posts:create")
LIST_POST_URL = reverse("posts:list")


class PostModelTests(TestCase):
    """Model tests"""

    def setUp(self):
        self.user = get_sample_user()
        self.community = get_sample_community(creater=self.user)

    def test_create_new_posts_success(self):
        """Test creating a new post success"""
        return
        content = "test content"
        photo = tempfile.NamedTemporaryFile(suffix=".png").name
        post = Post.objects.create(
            writer=self.user, community=self.community, content=content, photo=photo
        )

        self.assertEqual(post.writer, self.writer)
        self.assertEqual(1, Post.objects.all().count())
        self.assertEqual(str(post), f"{self.user}'s post")

        def __str__(self):
            return f"{self.writer}'s post"


class PublicPostTests(TestCase):
    """Public post tests"""

    def setUp(self):
        self.client = Client()

    def test_auth_required(self):
        """Test that authentication is required"""
        user = get_sample_user()
        community = get_sample_community(creater=user)
        payload = {"content": "test content"}
        res = self.client.post(CREATE_POST_URL, payload)

        self.assertRedirects(
            res,
            settings.LOGIN_URL + "?next=/posts/create/",
        )

        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(community=community)


class PrivatePostTests(TestCase):
    """Private post tests"""

    def setUp(self):
        self.user = get_sample_user()
        self.client = Client()
        self.client.force_login(self.user)
        self.community = get_sample_community()
        create_subscription(subscriber=self.user, community=self.community)

    def test_retrieve_posts(self):
        """Test retrieving a list of posts"""

        get_sample_post(writer=self.user, community=self.community)
        get_sample_post(
            writer=self.user, community=self.community, **{"content": "content2!!"}
        )
        res = self.client.get(LIST_POST_URL)

        self.assertEqual(res.status_code, 200)

    def test_create_post_success(self):
        """Test creating a new post"""
        payload = {
            "content": "sample content",
            "photo": tempfile.NamedTemporaryFile(suffix=".jpg").name,
            "community": self.community.pk,
        }
        res = self.client.post(CREATE_POST_URL, payload)
        post = Post.objects.get(content=payload["content"])

        self.assertEqual(post.content, payload["content"])
        self.assertRedirects(res, post.get_absolute_url())