from django.contrib import admin
from django.test import TestCase

from reviews_app.models import Review


class ReviewAdminTests(TestCase):
    def test_review_is_registered_in_admin(self):
        self.assertIn(Review, admin.site._registry)
