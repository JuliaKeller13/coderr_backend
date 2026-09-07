from django.contrib.auth import get_user_model
from django.test import TestCase

from users.api.serializers import RegistrationSerializer
from users.models import Profile


User = get_user_model()


class RegistrationSerializerTests(TestCase):

    def test_registration_serializer_creates_user_and_profile(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "repeated_password": "testpassword",
            "type": "customer",
        }

        serializer = RegistrationSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        user = serializer.save()

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(
            user.profile.type,
            Profile.UserType.CUSTOMER,
        )

    def test_password_is_hashed(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "repeated_password": "testpassword",
            "type": "customer",
        }

        serializer = RegistrationSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        user = serializer.save()

        self.assertNotEqual(user.password, "testpassword")
        self.assertTrue(user.check_password("testpassword"))

    def test_passwords_must_match(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "repeated_password": "wrongpassword",
            "type": "customer",
        }

        serializer = RegistrationSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("repeated_password", serializer.errors)