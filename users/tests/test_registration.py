from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationTests(APITestCase):

    def test_registration_creates_user_successfully(self):
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer",
        }

        response = self.client.post(
            "/api/registration/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
