from django.urls import reverse
from django.test import TestCase, Client
from django.core.validators import ValidationError
from django.conf import settings

from core.tests.sample_objects import (
    get_sample_user,
    get_sample_community,
    get_sample_post,
    create_subscription,
)

from comments.models import Comment


CREATE_COMMENT_URL = reverse("comments:create")


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


class PublicCommentTests(TestCase):
    """Public comment tests"""

    def setUp(self):
        self.client = Client()
        self.user = get_sample_user()
        self.community = get_sample_community(creater=self.user)
        create_subscription(subscriber=self.user, community=self.community)
        self.post = get_sample_post(writer=self.user, community=self.community)

    def test_auth_required(self):
        """Test that authentication is required"""
        payload = {"comment": "test comment"}
        res = self.client.post(CREATE_COMMENT_URL, payload)

        self.assertRedirects(
            res,
            settings.LOGIN_URL + f"?next=/comments/create/",
        )

        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(comment=payload["comment"])


class PrivateCommentTests(TestCase):
    """Private comment tests"""

    def setUp(self):
        self.user = get_sample_user()
        self.client = Client()
        self.client.force_login(self.user)
        self.community = get_sample_community()
        create_subscription(subscriber=self.user, community=self.community)
        self.post = get_sample_post(writer=self.user, community=self.community)

    def test_create_comment_success(self):
        """Test creating a new comment"""
        payload = {
            "post_pk": self.post.pk,
            "comment": "Test comment",
        }
        res = self.client.post(CREATE_COMMENT_URL, payload)
        comment = Comment.objects.get(comment=payload["comment"])

        self.assertEqual(res.status_code, 302)
        self.assertEqual(comment.comment, payload["comment"])
