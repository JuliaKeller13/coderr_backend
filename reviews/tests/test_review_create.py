from rest_framework import status

from reviews.models import Review

from .base import ReviewAPITestBase


class ReviewCreateTests(ReviewAPITestBase):

    def test_customer_can_create_review(self):
        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.post(
            "/api/reviews/",
            {
                "business_user": self.business_user.id,
                "rating": 4,
                "description": "Alles war toll!",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Review.objects.count(),
            1,
        )

        review = Review.objects.first()

        self.assertEqual(
            review.reviewer,
            self.customer_user,
        )

        self.assertEqual(
            review.business_user,
            self.business_user,
        )

        self.assertEqual(
            review.rating,
            4,
        )