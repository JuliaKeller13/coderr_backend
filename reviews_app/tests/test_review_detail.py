from rest_framework import status

from reviews_app.models import Review

from .base import ReviewAPITestBase


class ReviewDetailTests(ReviewAPITestBase):

    def create_review(self):
        return Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=4,
            description="Sehr guter Service.",
        )

    def test_owner_can_update_review(self):
        review = self.create_review()

        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.patch(
            f"/api/reviews/{review.id}/",
            {
                "rating": 5,
                "description": "Noch besser als erwartet!",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        review.refresh_from_db()

        self.assertEqual(review.rating, 5)
        self.assertEqual(
            review.description,
            "Noch besser als erwartet!",
        )

    def test_non_owner_cannot_update_review(self):
        review = self.create_review()

        other_customer = self.create_customer_user(
            username="othercustomer"
        )

        self.client.force_authenticate(
            user=other_customer
        )

        response = self.client.patch(
            f"/api/reviews/{review.id}/",
            {
                "rating": 5,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_unauthenticated_user_cannot_update_review(self):
        review = self.create_review()

        response = self.client.patch(
            f"/api/reviews/{review.id}/",
            {
                "rating": 5,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_unallowed_field_returns_400(self):
        review = self.create_review()

        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.patch(
            f"/api/reviews/{review.id}/",
            {
                "business_user": self.business_user.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_update_unknown_review_returns_404(self):
        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.patch(
            "/api/reviews/99999/",
            {
                "rating": 5,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_owner_can_delete_review(self):
        review = self.create_review()

        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.delete(
            f"/api/reviews/{review.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Review.objects.filter(
                pk=review.id
            ).exists()
        )

    def test_non_owner_cannot_delete_review(self):
        review = self.create_review()

        other_customer = self.create_customer_user(
            username="othercustomer"
        )

        self.client.force_authenticate(
            user=other_customer
        )

        response = self.client.delete(
            f"/api/reviews/{review.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_unauthenticated_user_cannot_delete_review(self):
        review = self.create_review()

        response = self.client.delete(
            f"/api/reviews/{review.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_delete_unknown_review_returns_404(self):
        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.delete(
            "/api/reviews/99999/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_rating_update_must_be_between_one_and_five(self):
        review = self.create_review()
        self.client.force_authenticate(user=self.customer_user)

        for rating in (0, 6):
            response = self.client.patch(
                f"/api/reviews/{review.id}/",
                {"rating": rating},
                format="json",
            )
            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
            )
