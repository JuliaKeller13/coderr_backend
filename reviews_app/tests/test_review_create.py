from rest_framework import status

from reviews_app.models import Review

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

    def test_business_user_cannot_create_review(self):
        self.client.force_authenticate(
            user=self.business_user
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
            status.HTTP_403_FORBIDDEN,
        )


    def test_unauthenticated_user_cannot_create_review(self):
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
            status.HTTP_401_UNAUTHORIZED,
        )


    def test_customer_cannot_review_same_business_twice(self):
        self.client.force_authenticate(
            user=self.customer_user
        )

        data = {
            "business_user": self.business_user.id,
            "rating": 4,
            "description": "Alles war toll!",
        }

        first_response = self.client.post(
            "/api/reviews/",
            data,
            format="json",
        )

        second_response = self.client.post(
            "/api/reviews/",
            data,
            format="json",
        )

        self.assertEqual(
            first_response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            second_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(
            Review.objects.count(),
            1,
        )


    def test_review_can_only_target_business_user(self):
        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.post(
            "/api/reviews/",
            {
                "business_user": self.customer_user.id,
                "rating": 4,
                "description": "Ungültig",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_rating_must_be_between_one_and_five(self):
        self.client.force_authenticate(
            user=self.customer_user
        )

        for rating in (0, 6):
            response = self.client.post(
                "/api/reviews/",
                {
                    "business_user": self.business_user.id,
                    "rating": rating,
                    "description": "Invalid rating",
                },
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
            )
