import datetime

from django.test import TestCase
from django.utils import timezone

from tests.factories import create_user


class SibylTestCase(TestCase):
    def make_user(self, username="testuser", password="testpass123", **kwargs):
        return create_user(username=username, password=password, **kwargs)

    def login(self, user):
        self.client.force_login(user)

    def today(self):
        return timezone.localdate()

    def days_from_today(self, days):
        return timezone.localdate() + datetime.timedelta(days=days)
