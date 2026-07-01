import datetime

from django.urls import reverse

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


class EventEditTest(SibylTestCase):
    def setUp(self):
        self.user = self.make_user()
        self.login(self.user)
        self.event = Event.objects.create(
            title="Original",
            owner=self.user,
            date=datetime.date(2026, 3, 1),
            time=datetime.time(14, 0),
        )

    def test_get_returns_200(self):
        response = self.client.get(reverse("events:edit", args=[self.event.pk]))
        self.assertEqual(response.status_code, 200)

    def test_get_form_prefilled_with_current_data(self):
        response = self.client.get(reverse("events:edit", args=[self.event.pk]))
        self.assertEqual(response.context["form"]["title"].value(), "Original")
        self.assertEqual(
            response.context["form"]["date"].value(), datetime.date(2026, 3, 1)
        )
        self.assertEqual(response.context["form"]["time"].value(), datetime.time(14, 0))

    def test_post_valid_updates_title(self):
        self.client.post(
            reverse("events:edit", args=[self.event.pk]),
            {"title": "Atualizado", "date": "2026-03-01", "time": ""},
        )
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, "Atualizado")

    def test_post_valid_updates_date(self):
        self.client.post(
            reverse("events:edit", args=[self.event.pk]),
            {"title": "Original", "date": "2026-06-15", "time": ""},
        )
        self.event.refresh_from_db()
        self.assertEqual(self.event.date, datetime.date(2026, 6, 15))

    def test_post_valid_updates_time(self):
        self.client.post(
            reverse("events:edit", args=[self.event.pk]),
            {"title": "Original", "date": "2026-03-01", "time": "09:30"},
        )
        self.event.refresh_from_db()
        self.assertEqual(self.event.time, datetime.time(9, 30))

    def test_post_valid_clears_time(self):
        self.client.post(
            reverse("events:edit", args=[self.event.pk]),
            {"title": "Original", "date": "2026-03-01", "time": ""},
        )
        self.event.refresh_from_db()
        self.assertIsNone(self.event.time)

    def test_post_valid_redirects_to_index(self):
        response = self.client.post(
            reverse("events:edit", args=[self.event.pk]),
            {"title": "Atualizado", "date": "2026-03-01", "time": ""},
        )
        self.assertRedirects(response, reverse("events:index"))

    def test_post_empty_title_returns_200(self):
        response = self.client.post(
            reverse("events:edit", args=[self.event.pk]),
            {"title": "", "date": "2026-03-01", "time": ""},
        )
        self.assertEqual(response.status_code, 200)

    def test_post_empty_date_returns_200(self):
        response = self.client.post(
            reverse("events:edit", args=[self.event.pk]),
            {"title": "Original", "date": "", "time": ""},
        )
        self.assertEqual(response.status_code, 200)

    def test_post_invalid_does_not_save(self):
        self.client.post(
            reverse("events:edit", args=[self.event.pk]),
            {"title": "", "date": "", "time": ""},
        )
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, "Original")
        self.assertEqual(self.event.date, datetime.date(2026, 3, 1))

    def test_get_other_users_event_returns_404(self):
        other = self.make_user(username="other")
        other_event = Event.objects.create(
            title="Other", owner=other, date=datetime.date(2026, 3, 1)
        )
        response = self.client.get(reverse("events:edit", args=[other_event.pk]))
        self.assertEqual(response.status_code, 404)

    def test_post_other_users_event_returns_404(self):
        other = self.make_user(username="other")
        other_event = Event.objects.create(
            title="Other", owner=other, date=datetime.date(2026, 3, 1)
        )
        response = self.client.post(
            reverse("events:edit", args=[other_event.pk]),
            {"title": "Hacked", "date": "2026-03-01", "time": ""},
        )
        self.assertEqual(response.status_code, 404)
        other_event.refresh_from_db()
        self.assertEqual(other_event.title, "Other")

    def test_edit_does_not_change_owner(self):
        self.client.post(
            reverse("events:edit", args=[self.event.pk]),
            {"title": "Atualizado", "date": "2026-03-01", "time": ""},
        )
        self.event.refresh_from_db()
        self.assertEqual(self.event.owner, self.user)
