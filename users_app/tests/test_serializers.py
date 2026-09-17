from django.contrib.auth import get_user_model
from django.test import TestCase

from users_app.api.serializers import ProfileSerializer, RegistrationSerializer
from users_app.models import Profile

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

class ProfileSerializerTests(TestCase):

    def test_profile_serializer_returns_user_and_profile_data(self):
        user = User.objects.create_user(
            username="businessuser",
            email="business@example.com",
            password="testpassword",
            first_name="Max",
            last_name="Mustermann",
        )

        profile = Profile.objects.create(
            user=user,
            type=Profile.UserType.BUSINESS,
            location="Iserlohn",
            tel="0123456789",
            description="Web developer",
            working_hours="9-17",
        )

        serializer = ProfileSerializer(profile)

        data = serializer.data

        self.assertEqual(data["user"], user.id)
        self.assertEqual(data["username"], "businessuser")
        self.assertEqual(data["first_name"], "Max")
        self.assertEqual(data["last_name"], "Mustermann")
        self.assertEqual(data["email"], "business@example.com")
        self.assertEqual(data["type"], "business")
        self.assertEqual(data["location"], "Iserlohn")
        self.assertEqual(data["tel"], "0123456789")
        self.assertEqual(data["description"], "Web developer")
        self.assertEqual(data["working_hours"], "9-17")
        self.assertIn("created_at", data)

    def test_profile_serializer_updates_user_and_profile_data(self):
        user = User.objects.create_user(
            username="businessuser",
            email="old@example.com",
            password="testpassword",
            first_name="Max",
            last_name="Mustermann",
        )

        profile = Profile.objects.create(
            user=user,
            type=Profile.UserType.BUSINESS,
            location="Iserlohn",
            tel="0123456789",
            description="Old description",
            working_hours="9-17",
        )

        data = {
            "first_name": "Maria",
            "last_name": "Musterfrau",
            "email": "new@example.com",
            "location": "Hamburg",
            "tel": "0987654321",
            "description": "Updated description",
            "working_hours": "10-18",
        }

        serializer = ProfileSerializer(
            profile,
            data=data,
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        serializer.save()

        user.refresh_from_db()
        profile.refresh_from_db()

        self.assertEqual(user.first_name, "Maria")
        self.assertEqual(user.last_name, "Musterfrau")
        self.assertEqual(user.email, "new@example.com")

        self.assertEqual(profile.location, "Hamburg")
        self.assertEqual(profile.tel, "0987654321")
        self.assertEqual(
            profile.description,
            "Updated description",
        )
        self.assertEqual(profile.working_hours, "10-18")
