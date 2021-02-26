from django.test import TestCase
from django.core.validators import ValidationError

from core.tests.sample_objects import (
    get_sample_user,
    get_sample_community,
    get_sample_post,
)

from comments.models import Comment


class CommentModelTests(TestCase):
    """Model test"""

    def setUp(self):
        self.user = get_sample_user()
        self.community = get_sample_community(creater=self.user)
        self.post = get_sample_post(writer=self.user, community=self.community)

    def test_create_new_comment_success(self):
        """Test creating a new comment success"""
        writer = self.user
        comment = "this is test comment"
        post = self.post

        comment_obj = Comment.objects.create(
            writer=self.user, post=post, comment=comment
        )

        self.assertEqual(comment_obj.writer, writer)
        self.assertEqual(1, Comment.objects.all().count())
        self.assertEqual(str(comment_obj), f"{writer}'s comment: {comment[:10]}...")

    def test_create_new_comment_invalid_field(self):
        """Test creating a new comment with invalid fields"""

        writer = self.user
        comment = ""
        post = self.post

        with self.assertRaises(ValidationError):
            Comment.objects.create(writer=writer, post=post, comment=comment)
