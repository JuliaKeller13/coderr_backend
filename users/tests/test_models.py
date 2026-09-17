from django.contrib.auth import get_user_model
from django.test import TestCase

from users.models import Profile


User = get_user_model()


class ProfileModelTests(TestCase):

    def test_profile_is_linked_to_user_and_stores_type(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

        profile = Profile.objects.create(
            user=user,
            type="customer",
        )

        self.assertEqual(profile.user, user)
        self.assertEqual(profile.type, "customer")
        self.assertEqual(user.profile, profile)

    def test_profile_fields_have_expected_defaults(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

        profile = Profile.objects.create(
            user=user,
            type=Profile.UserType.CUSTOMER,
        )

        self.assertEqual(profile.location, "")
        self.assertEqual(profile.tel, "")
        self.assertEqual(profile.description, "")
        self.assertEqual(profile.working_hours, "")
        self.assertIsNotNone(profile.created_at)

    def test_profile_string_representation(self):
        user = User.objects.create_user(
            username="julia",
            password="testpassword",
        )
        profile = Profile.objects.create(
            user=user,
            type=Profile.UserType.BUSINESS,
        )

        self.assertEqual(str(profile), "julia - business")