from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()


class LoginTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

    def test_login_returns_token_and_user_data(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
        }

        response = self.client.post(
            "/api/login/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("token", response.data)
        self.assertEqual(
            response.data["username"],
            "testuser",
        )
        self.assertEqual(
            response.data["email"],
            "test@example.com",
        )
        self.assertEqual(
            response.data["user_id"],
            self.user.id,
        )

        self.assertTrue(
            Token.objects.filter(
                user=self.user
            ).exists()
        )

    def test_login_with_wrong_password_returns_400(self):
        data = {
            "username": "testuser",
            "password": "wrongpassword",
        }

        response = self.client.post(
            "/api/login/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
