from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Profile


User = get_user_model()


class ProfileTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="businessuser",
            email="business@example.com",
            password="testpassword",
            first_name="Max",
            last_name="Mustermann",
        )

        self.profile = Profile.objects.create(
            user=self.user,
            type=Profile.UserType.BUSINESS,
            location="Iserlohn",
            tel="0123456789",
            description="Web developer",
            working_hours="9-17",
        )

    def test_authenticated_user_can_retrieve_profile(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            f"/api/profile/{self.user.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(response.data["user"], self.user.id)
        self.assertEqual(
            response.data["username"],
            "businessuser",
        )
        self.assertEqual(response.data["first_name"], "Max")
        self.assertEqual(response.data["last_name"], "Mustermann")
        self.assertEqual(
            response.data["email"],
            "business@example.com",
        )
        self.assertEqual(response.data["type"], "business")
        self.assertEqual(response.data["location"], "Iserlohn")

    def test_unauthenticated_user_cannot_retrieve_profile(self):
        response = self.client.get(
            f"/api/profile/{self.user.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_non_existing_profile_returns_404(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            "/api/profile/99999/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_user_can_update_own_profile(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "first_name": "Maria",
            "last_name": "Musterfrau",
            "location": "Hamburg",
            "tel": "0987654321",
            "description": "Updated description",
            "working_hours": "10-18",
            "email": "updated@example.com",
        }

        response = self.client.patch(
            f"/api/profile/{self.user.id}/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.user.refresh_from_db()
        self.profile.refresh_from_db()

        self.assertEqual(self.user.first_name, "Maria")
        self.assertEqual(self.user.last_name, "Musterfrau")
        self.assertEqual(
            self.user.email,
            "updated@example.com",
        )

        self.assertEqual(self.profile.location, "Hamburg")
        self.assertEqual(
            self.profile.description,
            "Updated description",
        )

    def test_user_cannot_update_another_users_profile(self):
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="testpassword",
        )

        Profile.objects.create(
            user=other_user,
            type=Profile.UserType.CUSTOMER,
        )

        self.client.force_authenticate(user=other_user)

        data = {
            "first_name": "Hacked",
        }

        response = self.client.patch(
            f"/api/profile/{self.user.id}/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.first_name,
            "Max",
        )

    def test_authenticated_user_can_list_business_profiles(self):
        customer_user = User.objects.create_user(
            username="customeruser",
            email="customer@example.com",
            password="testpassword",
        )

        Profile.objects.create(
            user=customer_user,
            type=Profile.UserType.CUSTOMER,
        )

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            "/api/profiles/business/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["type"],
            Profile.UserType.BUSINESS,
        )

    def test_authenticated_user_can_list_customer_profiles(self):
        customer_user = User.objects.create_user(
            username="customeruser",
            email="customer@example.com",
            password="testpassword",
        )

        Profile.objects.create(
            user=customer_user,
            type=Profile.UserType.CUSTOMER,
        )

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            "/api/profiles/customer/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["type"],
            Profile.UserType.CUSTOMER,
        )

    def test_unauthenticated_user_cannot_list_business_profiles(self):
        response = self.client.get(
            "/api/profiles/business/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_unauthenticated_user_cannot_list_customer_profiles(self):
        response = self.client.get(
            "/api/profiles/customer/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )