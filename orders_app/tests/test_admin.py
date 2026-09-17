from django.contrib import admin
from django.test import TestCase

from orders_app.models import Order


class OrderAdminTests(TestCase):
    def test_order_is_registered_in_admin(self):
        self.assertIn(Order, admin.site._registry)
