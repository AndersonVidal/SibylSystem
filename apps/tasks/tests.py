import datetime
from unittest.mock import patch

from apps.tasks.models import Task
from tests.base import SibylTestCase

FIXED_TODAY = datetime.date(2026, 1, 15)
YESTERDAY = datetime.date(2026, 1, 14)
TOMORROW = datetime.date(2026, 1, 16)


class TaskQuerySetOverdueTest(SibylTestCase):
    def setUp(self):
        self.user = self.make_user()

    def _task(self, **kwargs):
        return Task.objects.create(title="t", owner=self.user, **kwargs)

    def _qs(self):
        return Task.objects.filter(owner=self.user).overdue(today=FIXED_TODAY)

    def test_pending_yesterday_returned(self):
        self._task(due_date=YESTERDAY)
        self.assertEqual(self._qs().count(), 1)

    def test_pending_today_not_returned(self):
        self._task(due_date=FIXED_TODAY)
        self.assertFalse(self._qs().exists())

    def test_pending_tomorrow_not_returned(self):
        self._task(due_date=TOMORROW)
        self.assertFalse(self._qs().exists())

    def test_pending_no_due_date_not_returned(self):
        self._task()
        self.assertFalse(self._qs().exists())

    def test_completed_yesterday_not_returned(self):
        self._task(due_date=YESTERDAY, status=Task.Status.COMPLETED)
        self.assertFalse(self._qs().exists())

    def test_other_user_task_not_returned(self):
        other = self.make_user(username="other")
        Task.objects.create(title="t", owner=other, due_date=YESTERDAY)
        self.assertFalse(self._qs().exists())


class TaskQuerySetPendingNotOverdueTest(SibylTestCase):
    def setUp(self):
        self.user = self.make_user()

    def _task(self, **kwargs):
        return Task.objects.create(title="t", owner=self.user, **kwargs)

    def _qs(self):
        return Task.objects.filter(owner=self.user).pending_not_overdue(
            today=FIXED_TODAY
        )

    def test_pending_no_due_date_returned(self):
        self._task()
        self.assertEqual(self._qs().count(), 1)

    def test_pending_today_returned(self):
        self._task(due_date=FIXED_TODAY)
        self.assertEqual(self._qs().count(), 1)

    def test_pending_tomorrow_returned(self):
        self._task(due_date=TOMORROW)
        self.assertEqual(self._qs().count(), 1)

    def test_pending_yesterday_not_returned(self):
        self._task(due_date=YESTERDAY)
        self.assertFalse(self._qs().exists())

    def test_completed_not_returned(self):
        self._task(status=Task.Status.COMPLETED)
        self.assertFalse(self._qs().exists())

    def test_other_user_task_not_returned(self):
        other = self.make_user(username="other")
        Task.objects.create(title="t", owner=other)
        self.assertFalse(self._qs().exists())


class TaskIsOverdueTest(SibylTestCase):
    def setUp(self):
        self.user = self.make_user()

    def _task(self, **kwargs):
        return Task.objects.create(title="t", owner=self.user, **kwargs)

    def test_pending_yesterday_is_true(self):
        task = self._task(due_date=YESTERDAY)
        with patch("apps.tasks.models.timezone.localdate", return_value=FIXED_TODAY):
            self.assertTrue(task.is_overdue)

    def test_pending_today_is_false(self):
        task = self._task(due_date=FIXED_TODAY)
        with patch("apps.tasks.models.timezone.localdate", return_value=FIXED_TODAY):
            self.assertFalse(task.is_overdue)

    def test_pending_tomorrow_is_false(self):
        task = self._task(due_date=TOMORROW)
        with patch("apps.tasks.models.timezone.localdate", return_value=FIXED_TODAY):
            self.assertFalse(task.is_overdue)

    def test_pending_no_due_date_is_false(self):
        task = self._task()
        with patch("apps.tasks.models.timezone.localdate", return_value=FIXED_TODAY):
            self.assertFalse(task.is_overdue)

    def test_completed_yesterday_is_false(self):
        task = self._task(due_date=YESTERDAY, status=Task.Status.COMPLETED)
        with patch("apps.tasks.models.timezone.localdate", return_value=FIXED_TODAY):
            self.assertFalse(task.is_overdue)
