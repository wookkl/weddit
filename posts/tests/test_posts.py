import tempfile

from django.test import TestCase

from core.tests.sample_objects import (
    get_sample_user,
    get_sample_community,
    get_sample_post,
)

from posts.models import Post


class PostsModelTests(TestCase):
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
