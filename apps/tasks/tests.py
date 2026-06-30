import datetime
from unittest.mock import patch

from django.urls import reverse

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


class TaskEditTest(SibylTestCase):
    def setUp(self):
        self.user = self.make_user()
        self.login(self.user)
        self.task = Task.objects.create(
            title="Original",
            owner=self.user,
            due_date=datetime.date(2026, 3, 1),
        )

    def test_get_returns_200(self):
        response = self.client.get(reverse("tasks:edit", args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)

    def test_get_form_prefilled_with_current_data(self):
        response = self.client.get(reverse("tasks:edit", args=[self.task.pk]))
        self.assertEqual(response.context["form"]["title"].value(), "Original")
        self.assertEqual(
            response.context["form"]["due_date"].value(), datetime.date(2026, 3, 1)
        )

    def test_post_valid_updates_title(self):
        self.client.post(
            reverse("tasks:edit", args=[self.task.pk]),
            {"title": "Atualizado", "due_date": ""},
        )
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Atualizado")

    def test_post_valid_updates_due_date(self):
        self.client.post(
            reverse("tasks:edit", args=[self.task.pk]),
            {"title": "Original", "due_date": "2026-06-01"},
        )
        self.task.refresh_from_db()
        self.assertEqual(self.task.due_date, datetime.date(2026, 6, 1))

    def test_post_valid_redirects_to_index(self):
        response = self.client.post(
            reverse("tasks:edit", args=[self.task.pk]),
            {"title": "Atualizado", "due_date": ""},
        )
        self.assertRedirects(response, reverse("tasks:index"))

    def test_post_empty_title_returns_200(self):
        response = self.client.post(
            reverse("tasks:edit", args=[self.task.pk]),
            {"title": "", "due_date": ""},
        )
        self.assertEqual(response.status_code, 200)

    def test_post_empty_title_does_not_save(self):
        self.client.post(
            reverse("tasks:edit", args=[self.task.pk]),
            {"title": "", "due_date": ""},
        )
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Original")

    def test_get_other_users_task_returns_404(self):
        other = self.make_user(username="other")
        other_task = Task.objects.create(title="Other", owner=other)
        response = self.client.get(reverse("tasks:edit", args=[other_task.pk]))
        self.assertEqual(response.status_code, 404)

    def test_post_other_users_task_returns_404(self):
        other = self.make_user(username="other")
        other_task = Task.objects.create(title="Other", owner=other)
        response = self.client.post(
            reverse("tasks:edit", args=[other_task.pk]),
            {"title": "Hacked", "due_date": ""},
        )
        self.assertEqual(response.status_code, 404)
        other_task.refresh_from_db()
        self.assertEqual(other_task.title, "Other")

    def test_edit_does_not_change_status(self):
        completed = Task.objects.create(
            title="Concluída", owner=self.user, status=Task.Status.COMPLETED
        )
        self.client.post(
            reverse("tasks:edit", args=[completed.pk]),
            {"title": "Concluída Editada", "due_date": ""},
        )
        completed.refresh_from_db()
        self.assertEqual(completed.status, Task.Status.COMPLETED)

    def test_edit_does_not_change_owner(self):
        self.client.post(
            reverse("tasks:edit", args=[self.task.pk]),
            {"title": "Atualizado", "due_date": ""},
        )
        self.task.refresh_from_db()
        self.assertEqual(self.task.owner, self.user)
