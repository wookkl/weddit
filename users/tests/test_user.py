from django.test import TestCase
from django.core.validators import ValidationError

from users import models


class ModelTests(TestCase):
    """Model test"""

    def test_create_new_user_successfully(self):
        """Test creating a new user successfully"""
        email = "test@gmail.com"
        nickname = "test name"
        password = "password123@"
        user = models.User.objects.create_user(
            email=email, nickname=nickname, password=password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.nickname, nickname)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_new_user_invalid(self):
        """Test creating a new user with invalid email"""

        with self.assertRaises(ValidationError):
            models.User.objects.create_user(
                email=None,
                nickname="test name",
                password="password123@",
            )

    def test_create_new_superuser_sucessfully(self):
        """Test creating a new superuser sucessfully"""

        email = "superuser@gmail.com"
        nickname = "admin"
        password = "superuserpassword123@"

        superuser = models.User.objects.create_superuser(
            email=email,
            nickname=nickname,
            password=password,
        )

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
