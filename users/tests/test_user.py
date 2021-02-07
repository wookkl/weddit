from django.test import TestCase, Client
from django.core.validators import ValidationError
from django.urls import reverse
from django.contrib.auth import get_user_model

SIGN_UP_URL = reverse("sign-up")
LOGOUT_URL = reverse("logout")
UPDATE_EMAIL_URL = reverse("update-email")
UPDATE_NICKNAME_URL = reverse("update-nickname")
UPDATE_PASSWORD_URL = reverse("update-password")


def get_user_retrieve_url(nickname):
    return reverse("user:detail", kwargs={"nickname": nickname})


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class UserModelTests(TestCase):
    """Model test"""

    def test_create_new_user_success(self):
        """Test creating a new user success"""
        email = "test@gmail.com"
        nickname = "testname"
        password = "password123@"
        user = get_user_model().objects.create_user(
            email=email, nickname=nickname, password=password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.nickname, nickname)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_new_user_invalid(self):
        """Test creating a new user with invalid fields"""

        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                email=None,
                nickname="testname",
                password="password123@",
            )

        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                email="test@gmail.com",
                nickname="test     name",
                password="password123@",
            )

    def test_create_new_superuser_success(self):
        """Test creating a new superuser sucessfully"""

        email = "superuser@gmail.com"
        nickname = "admin"
        password = "superuserpassword123@"

        superuser = get_user_model().objects.create_superuser(
            email=email,
            nickname=nickname,
            password=password,
        )

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


class PublicUserTests(TestCase):
    """Public user test"""

    def setUp(self):
        self.client = Client()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""

        payload = {
            "email": "test@gmail.com",
            "nickname": "testname",
            "password1": "userpass123@",
            "password2": "userpass123@",
        }

        res = self.client.post(SIGN_UP_URL, payload)

        self.assertEqual(res.status_code, 302)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password1"]))

    def test_user_exist(self):
        """Test creating user that already exists fails"""

        payload = {
            "email": "test@gmail.com",
            "nickname": "John",
            "password1": "userpass123@",
            "password2": "userpass123@",
        }

        create_user(
            **{
                "email": "test@gmail.com",
                "nickname": "John",
                "password": "userpass123@",
            }
        )

        self.client.post(SIGN_UP_URL, payload)

        self.assertEqual(1, get_user_model().objects.count())

    def test_paasword_too_short(self):
        payload = {
            "email": "test@gmail.com",
            "nickname": "John",
            "password1": "123",
            "password2": "123",
        }

        self.client.post(SIGN_UP_URL, payload)

        self.assertFalse(
            get_user_model().objects.filter(email=payload["email"]).exists()
        )


class PrivateUserTests(TestCase):
    """Private user test"""

    def setUp(self):
        self.client = Client()
        self.user = create_user(
            **{
                "email": "test@gmail.com",
                "nickname": "testname",
                "password": "password123@",
            }
        )
        self.client.force_login(self.user)

    def test_retrieve_user(self):
        res = self.client.get(get_user_retrieve_url(self.user.nickname))

        self.assertEqual(res.status_code, 200)

    def test_logout_user(self):
        res = self.client.get(LOGOUT_URL)

        self.assertEqual(res.status_code, 302)

    def test_update_new_email_success(self):
        """Test updating a new email success"""
        payload = {"new_email": "newemail@gmail.com", "password": "password123@"}

        res = self.client.post(UPDATE_EMAIL_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, payload["new_email"])
        self.assertEqual(res.status_code, 302)

    def test_update_new_email_invalid(self):
        """Test updating email that already exists fails"""
        create_user(
            **{
                "email": "newemail@gmail.com",
                "nickname": "newname",
                "password": "password123@",
            }
        )
        payload = {"new_email": "newemail@gmail.com", "password": "password123@"}
        self.client.post(UPDATE_EMAIL_URL, payload)
        self.user.refresh_from_db()
        self.assertFalse(self.user.email == payload["new_email"])

    def test_update_new_nickname_success(self):
        """Test updating a new nickname success"""
        payload = {"new_nickname": "changednickname"}

        res = self.client.post(UPDATE_NICKNAME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(res.status_code, 302)
        self.assertEqual(self.user.nickname, payload["new_nickname"])

    def test_update_new_nickname_invalid(self):
        """Test updating nickname that already exists fails"""
        create_user(
            **{
                "email": "newemail@gmail.com",
                "nickname": "samename",
                "password": "password123@",
            }
        )
        payload = {"new_nickname": "samename"}
        self.client.post(UPDATE_NICKNAME_URL, payload)
        self.user.refresh_from_db()
        self.assertFalse(self.user.nickname == payload["new_nickname"])

    def test_update_new_password_success(self):
        """Test updating a new password success"""
        payload = {
            "current_password": "password123@",
            "password1": "changedpassword123@",
            "password2": "changedpassword123@",
        }

        res = self.client.post(UPDATE_PASSWORD_URL, payload)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload["password1"]))
        self.assertEqual(res.status_code, 302)

    def test_update_new_password_invalid(self):
        """Test updating with mismatched password"""
        payload = {
            "current_password": "wrongpassword123@",
            "password1": "password49124@",
            "password2": "password49124@",
        }
        self.client.post(UPDATE_PASSWORD_URL, payload)
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password(payload["password1"]))
