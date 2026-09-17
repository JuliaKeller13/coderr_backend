from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from reviews.models import Review
from users.models import Profile


User = get_user_model()


class ReviewModelTests(TestCase):

    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer",
            password="testpassword",
        )

        Profile.objects.create(
            user=self.customer,
            type=Profile.UserType.CUSTOMER,
        )

        self.business = User.objects.create_user(
            username="business",
            password="testpassword",
        )

        Profile.objects.create(
            user=self.business,
            type=Profile.UserType.BUSINESS,
        )

    def test_review_can_be_created(self):
        review = Review.objects.create(
            business_user=self.business,
            reviewer=self.customer,
            rating=4,
            description="Sehr professioneller Service.",
        )

        self.assertEqual(
            review.business_user,
            self.business,
        )
        self.assertEqual(
            review.reviewer,
            self.customer,
        )
        self.assertEqual(
            review.rating,
            4,
        )

        self.assertEqual(
            str(review),
            "customer -> business",
        )

    def test_reviewer_can_only_review_business_once(self):
        Review.objects.create(
            business_user=self.business,
            reviewer=self.customer,
            rating=4,
            description="Sehr gut.",
        )

        with self.assertRaises(IntegrityError):
            Review.objects.create(
                business_user=self.business,
                reviewer=self.customer,
                rating=5,
                description="Noch eine Bewertung.",
            )
