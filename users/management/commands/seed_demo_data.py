from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from users.models import Profile


User = get_user_model()

DEMO_USERS = [
    {
        "username": "andrey",
        "password": "asdasd",
        "email": "andrey@example.com",
        "first_name": "Andrey",
        "last_name": "Customer",
        "profile": {
            "type": Profile.UserType.CUSTOMER,
        },
    },
    {
        "username": "kevin",
        "password": "asdasd24",
        "email": "kevin@example.com",
        "first_name": "Kevin",
        "last_name": "Business",
        "profile": {
            "type": Profile.UserType.BUSINESS,
            "location": "Berlin",
            "description": (
                "Full-stack developer and web designer focused on "
                "modern and user-friendly web applications."
            ),
            "working_hours": "Mon-Fri, 09:00-17:00",
        },
    },
]


class Command(BaseCommand):
    help = "Create or update demo users for the guest login."

    def handle(self, *args, **options):
        for data in DEMO_USERS:
            self._create_demo_user(data)
        self.stdout.write(self.style.SUCCESS("Demo users are ready."))

    def _create_demo_user(self, data):
        user, _ = User.objects.get_or_create(username=data["username"])
        user.email = data["email"]
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.set_password(data["password"])
        user.save()
        Profile.objects.update_or_create(
            user=user,
            defaults=data["profile"],
        )