from django.test import TestCase, Client


class PublicUserTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_create_successfully(self):
        payload = {
            "email": "test@gmail.com",
            "password1": "password123@",
            "password2": "password123@",
        }
