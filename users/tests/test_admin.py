from django.contrib import admin
from django.test import TestCase

from users.models import Profile


class ProfileAdminTests(TestCase):
    def test_profile_is_registered_in_admin(self):
        self.assertIn(Profile, admin.site._registry)
