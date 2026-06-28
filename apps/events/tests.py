import datetime

from apps.events.models import Event
from tests.base import SibylTestCase

FIXED_TODAY = datetime.date(2026, 1, 15)
YESTERDAY = datetime.date(2026, 1, 14)
TOMORROW = datetime.date(2026, 1, 16)
DAY_AFTER_TOMORROW = datetime.date(2026, 1, 17)


class EventQuerySetTodayTest(SibylTestCase):
    def setUp(self):
        self.user = self.make_user()

    def _event(self, date, **kwargs):
        return Event.objects.create(title="e", owner=self.user, date=date, **kwargs)

    def _qs(self):
        return Event.objects.filter(owner=self.user).today(today=FIXED_TODAY)

    def test_today_event_returned(self):
        self._event(FIXED_TODAY)
        self.assertEqual(self._qs().count(), 1)

    def test_yesterday_event_not_returned(self):
        self._event(YESTERDAY)
        self.assertFalse(self._qs().exists())

    def test_tomorrow_event_not_returned(self):
        self._event(TOMORROW)
        self.assertFalse(self._qs().exists())

    def test_other_user_event_not_returned(self):
        other = self.make_user(username="other")
        Event.objects.create(title="e", owner=other, date=FIXED_TODAY)
        self.assertFalse(self._qs().exists())


class EventQuerySetUpcomingTest(SibylTestCase):
    def setUp(self):
        self.user = self.make_user()

    def _event(self, date, **kwargs):
        return Event.objects.create(title="e", owner=self.user, date=date, **kwargs)

    def _qs(self):
        return Event.objects.filter(owner=self.user).upcoming(today=FIXED_TODAY)

    def test_tomorrow_event_returned(self):
        self._event(TOMORROW)
        self.assertEqual(self._qs().count(), 1)

    def test_day_after_tomorrow_event_returned(self):
        self._event(DAY_AFTER_TOMORROW)
        self.assertEqual(self._qs().count(), 1)

    def test_today_event_not_returned(self):
        self._event(FIXED_TODAY)
        self.assertFalse(self._qs().exists())

    def test_yesterday_event_not_returned(self):
        self._event(YESTERDAY)
        self.assertFalse(self._qs().exists())

    def test_other_user_event_not_returned(self):
        other = self.make_user(username="other")
        Event.objects.create(title="e", owner=other, date=TOMORROW)
        self.assertFalse(self._qs().exists())
