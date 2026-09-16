from rest_framework.permissions import BasePermission

from users.models import Profile


class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return (
            request.user.profile.type
            == Profile.UserType.CUSTOMER
        )