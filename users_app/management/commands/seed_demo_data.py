from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from offers_app.models import Offer, OfferDetail
from orders_app.models import Order
from reviews_app.models import Review
from users_app.models import Profile

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
            "location": "Hamburg",
            "description": "Product manager looking for reliable digital services.",
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
            "tel": "+49 30 55501234",
            "description": (
                "Full-stack developer and web designer focused on "
                "modern and user-friendly web applications."
            ),
            "working_hours": "Mon-Fri, 09:00-17:00",
        },
    },
    {
        "username": "lena",
        "password": "demo-lena-2026",
        "email": "lena@example.com",
        "first_name": "Lena",
        "last_name": "Schmidt",
        "profile": {"type": Profile.UserType.CUSTOMER, "location": "Munich"},
    },
    {
        "username": "marco",
        "password": "demo-marco-2026",
        "email": "marco@example.com",
        "first_name": "Marco",
        "last_name": "Fischer",
        "profile": {"type": Profile.UserType.CUSTOMER, "location": "Cologne"},
    },
    {
        "username": "sophia",
        "password": "demo-sophia-2026",
        "email": "sophia@example.com",
        "first_name": "Sophia",
        "last_name": "Wagner",
        "profile": {
            "type": Profile.UserType.BUSINESS,
            "location": "Hamburg",
            "tel": "+49 40 55502345",
            "description": (
                "Brand designer creating clear visual identities for "
                "growing companies."
            ),
            "working_hours": "Mon-Fri, 10:00-18:00",
        },
    },
    {
        "username": "jonas",
        "password": "demo-jonas-2026",
        "email": "jonas@example.com",
        "first_name": "Jonas",
        "last_name": "Weber",
        "profile": {
            "type": Profile.UserType.BUSINESS,
            "location": "Cologne",
            "tel": "+49 221 55503456",
            "description": (
                "Video editor and content creator for social media "
                "campaigns."
            ),
            "working_hours": "Tue-Sat, 09:00-17:00",
        },
    },
]

OFFER_DATA = [
    (
        "kevin",
        "Professional Website Development",
        "Custom websites for growing businesses.",
    ),
    ("kevin", "WordPress Website Setup", "A polished WordPress site ready for launch."),
    ("sophia", "Modern Logo Design", "A memorable logo designed for your brand."),
    (
        "sophia",
        "Complete Brand Identity",
        "A consistent visual identity across every touchpoint.",
    ),
    (
        "jonas",
        "Professional Video Editing",
        "Engaging edits for product and social videos.",
    ),
    (
        "jonas",
        "Social Media Content Package",
        "A practical set of short-form videos for your channels.",
    ),
]

DETAIL_DATA = {
    "Professional Website Development": [
        ("Starter website", 1, 7, "650.00", ["One-page layout", "Responsive design"]),
        (
            "Business website",
            2,
            14,
            "1200.00",
            ["Up to five pages", "Contact form", "SEO basics"],
        ),
        (
            "Advanced website",
            4,
            21,
            "2200.00",
            ["Custom sections", "CMS setup", "Analytics"],
        ),
    ],
    "WordPress Website Setup": [
        (
            "WordPress landing page",
            1,
            5,
            "450.00",
            ["Theme setup", "Mobile optimization"],
        ),
        (
            "WordPress business site",
            2,
            10,
            "900.00",
            ["Five pages", "Plugin configuration", "Training call"],
        ),
        (
            "WordPress growth site",
            4,
            16,
            "1650.00",
            ["Custom styling", "Blog setup", "Performance review"],
        ),
    ],
    "Modern Logo Design": [
        ("Logo concept", 1, 4, "180.00", ["One concept", "PNG delivery"]),
        ("Logo selection", 2, 7, "360.00", ["Three concepts", "Color variations"]),
        (
            "Logo master package",
            4,
            10,
            "650.00",
            ["Source files", "Print-ready formats", "Brand colors"],
        ),
    ],
    "Complete Brand Identity": [
        ("Brand starter", 1, 7, "550.00", ["Logo refinement", "Color palette"]),
        ("Brand system", 3, 14, "1100.00", ["Typography", "Logo suite", "Brand guide"]),
        (
            "Full identity",
            5,
            21,
            "2100.00",
            ["Complete brand guide", "Stationery", "Social templates"],
        ),
    ],
    "Professional Video Editing": [
        ("Short video edit", 1, 4, "220.00", ["Up to 60 seconds", "Basic cuts"]),
        (
            "Campaign video",
            2,
            8,
            "520.00",
            ["Up to three minutes", "Captions", "Sound mix"],
        ),
        (
            "Premium video edit",
            4,
            14,
            "950.00",
            ["Up to eight minutes", "Motion graphics", "Color grading"],
        ),
    ],
    "Social Media Content Package": [
        (
            "Social starter",
            1,
            5,
            "300.00",
            ["Three short videos", "Caption suggestions"],
        ),
        ("Social growth", 2, 10, "700.00", ["Eight short videos", "Thumbnail designs"]),
        (
            "Social campaign",
            4,
            16,
            "1350.00",
            ["Sixteen videos", "Content calendar", "Format variations"],
        ),
    ],
}

ORDER_DATA = [
    (
        "andrey",
        "kevin",
        "Professional Website Development",
        "standard",
        Order.Status.IN_PROGRESS,
    ),
    ("lena", "kevin", "WordPress Website Setup", "premium", Order.Status.COMPLETED),
    (
        "marco",
        "sophia",
        "Complete Brand Identity",
        "standard",
        Order.Status.IN_PROGRESS,
    ),
    ("andrey", "sophia", "Modern Logo Design", "basic", Order.Status.COMPLETED),
    ("lena", "jonas", "Professional Video Editing", "premium", Order.Status.CANCELLED),
    (
        "marco",
        "jonas",
        "Social Media Content Package",
        "standard",
        Order.Status.IN_PROGRESS,
    ),
]

REVIEW_DATA = [
    ("andrey", "kevin", 5, "Kevin translated our ideas into a fast, polished website."),
    (
        "lena",
        "kevin",
        4,
        "Clear communication and a very professional WordPress setup.",
    ),
    (
        "marco",
        "sophia",
        5,
        "Sophia created a brand identity that feels distinctive and flexible.",
    ),
    ("andrey", "sophia", 4, "The logo concepts were thoughtful and easy to apply."),
    (
        "lena",
        "jonas",
        5,
        "Jonas delivered energetic edits that work perfectly for social media.",
    ),
    (
        "marco",
        "jonas",
        4,
        "Reliable editing, strong pacing, and excellent attention to detail.",
    ),
]


class Command(BaseCommand):
    help = "Create or update demo users for the guest login."

    def handle(self, *args, **options):
        users = self._create_demo_users()
        offers = self._create_demo_offers(users)
        self._create_demo_orders(users, offers)
        self._create_demo_reviews(users)
        self.stdout.write(self.style.SUCCESS("Demo data is ready."))

    def _create_demo_users(self):
        return {data["username"]: self._create_demo_user(data) for data in DEMO_USERS}

    @staticmethod
    def _create_demo_user(data):
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
        return user

    def _create_demo_offers(self, users):
        offers = {}
        for username, title, description in OFFER_DATA:
            offer, _ = Offer.objects.update_or_create(
                user=users[username],
                title=title,
                defaults={"description": description, "image": None},
            )
            self._create_offer_details(offer)
            offers[title] = offer
        return offers

    @staticmethod
    def _create_offer_details(offer):
        details = zip(OfferDetail.OfferType.values, DETAIL_DATA[offer.title])
        for offer_type, detail in details:
            Command._update_offer_detail(offer, offer_type, detail)

    @staticmethod
    def _update_offer_detail(offer, offer_type, detail):
        title, revisions, days, price, features = detail
        OfferDetail.objects.update_or_create(
            offer=offer,
            offer_type=offer_type,
            defaults={
                "title": title,
                "revisions": revisions,
                "delivery_time_in_days": days,
                "price": price,
                "features": features,
            },
        )

    @staticmethod
    def _create_demo_orders(users, offers):
        for customer, business, title, offer_type, status in ORDER_DATA:
            detail = offers[title].details.get(offer_type=offer_type)
            Command._update_demo_order(
                users, customer, business, title, offer_type, status, detail
            )

    @staticmethod
    def _update_demo_order(
        users, customer, business, title, offer_type, status, detail
    ):
        defaults = Command._order_defaults(detail, status)
        Order.objects.update_or_create(
            customer_user=users[customer],
            business_user=users[business],
            title=title,
            offer_type=offer_type,
            defaults=defaults,
        )

    @staticmethod
    def _order_defaults(detail, status):
        return {
            "revisions": detail.revisions,
            "delivery_time_in_days": detail.delivery_time_in_days,
            "price": detail.price,
            "features": detail.features,
            "status": status,
        }

    @staticmethod
    def _create_demo_reviews(users):
        for reviewer, business, rating, description in REVIEW_DATA:
            Review.objects.update_or_create(
                reviewer=users[reviewer],
                business_user=users[business],
                defaults={"rating": rating, "description": description},
            )
