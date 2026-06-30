import datetime
from unittest.mock import patch

from django.urls import reverse
from django.utils import timezone

from apps.events.models import Event
from apps.goals.models import Goal
from apps.tasks.models import Task
from tests.base import SibylTestCase

FIXED_TODAY = datetime.date(2026, 1, 15)
FIXED_YESTERDAY = FIXED_TODAY - datetime.timedelta(days=1)
FIXED_TOMORROW = FIXED_TODAY + datetime.timedelta(days=1)


class TaskOwnerIsolationTest(SibylTestCase):
    def setUp(self):
        self.user_a = self.make_user(username="user_a")
        self.user_b = self.make_user(username="user_b")
        self.task = Task.objects.create(title="task_a", owner=self.user_a)

    def test_list_excludes_other_users_tasks(self):
        self.login(self.user_b)
        response = self.client.get(reverse("tasks:index"))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["tasks"].filter(pk=self.task.pk).exists())

    def test_complete_returns_404_for_other_users_task(self):
        self.login(self.user_b)
        response = self.client.post(reverse("tasks:complete", args=[self.task.pk]))
        self.assertEqual(response.status_code, 404)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.Status.PENDING)


class EventOwnerIsolationTest(SibylTestCase):
    def setUp(self):
        self.user_a = self.make_user(username="user_a")
        self.user_b = self.make_user(username="user_b")
        self.event = Event.objects.create(
            title="event_a", owner=self.user_a, date=timezone.localdate()
        )

    def test_list_excludes_other_users_events(self):
        self.login(self.user_b)
        response = self.client.get(reverse("events:index"))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["events"].filter(pk=self.event.pk).exists())


class GoalOwnerIsolationTest(SibylTestCase):
    def setUp(self):
        self.user_a = self.make_user(username="user_a")
        self.user_b = self.make_user(username="user_b")
        self.goal = Goal.objects.create(title="goal_a", owner=self.user_a, progress=50)

    def test_list_excludes_other_users_goals(self):
        self.login(self.user_b)
        response = self.client.get(reverse("goals:index"))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["goals"].filter(pk=self.goal.pk).exists())

    def test_update_progress_returns_404_for_other_users_goal(self):
        self.login(self.user_b)
        response = self.client.post(
            reverse("goals:update_progress", args=[self.goal.pk]),
            data={"progress": 100},
        )
        self.assertEqual(response.status_code, 404)
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.progress, 50)


class DashboardOwnerIsolationTest(SibylTestCase):
    def setUp(self):
        self.user_a = self.make_user(username="user_a")
        self.user_b = self.make_user(username="user_b")
        today = timezone.localdate()
        yesterday = today - datetime.timedelta(days=1)
        tomorrow = today + datetime.timedelta(days=1)
        Task.objects.create(title="pending_a", owner=self.user_a)
        Task.objects.create(title="overdue_a", owner=self.user_a, due_date=yesterday)
        Event.objects.create(title="today_event_a", owner=self.user_a, date=today)
        Event.objects.create(title="upcoming_event_a", owner=self.user_a, date=tomorrow)
        Goal.objects.create(title="goal_a", owner=self.user_a, progress=50)

    def test_dashboard_excludes_all_of_other_users_data(self):
        self.login(self.user_b)
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 200)
        ctx = response.context
        self.assertFalse(ctx["overdue_tasks"].exists())
        self.assertFalse(ctx["pending_tasks"].exists())
        self.assertFalse(ctx["today_events"].exists())
        self.assertFalse(ctx["upcoming_events"].exists())
        self.assertFalse(ctx["active_goals"].exists())


def _start_date_patches(test_case, fixed_date=FIXED_TODAY):
    for target in (
        "apps.tasks.models.timezone.localdate",
        "apps.events.models.timezone.localdate",
    ):
        p = patch(target, return_value=fixed_date)
        p.start()
        test_case.addCleanup(p.stop)


class DashboardContextTest(SibylTestCase):
    def setUp(self):
        self.user = self.make_user()
        self.login(self.user)
        other = self.make_user(username="other")

        self.overdue = Task.objects.create(
            title="overdue", owner=self.user, due_date=FIXED_YESTERDAY
        )
        self.pending_due_today = Task.objects.create(
            title="pending_due_today", owner=self.user, due_date=FIXED_TODAY
        )
        self.pending_future = Task.objects.create(
            title="pending_future", owner=self.user, due_date=FIXED_TOMORROW
        )
        self.pending_no_due = Task.objects.create(
            title="pending_no_due", owner=self.user
        )
        self.completed = Task.objects.create(
            title="completed",
            owner=self.user,
            status=Task.Status.COMPLETED,
            due_date=FIXED_YESTERDAY,
        )
        Task.objects.create(title="other_task", owner=other)

        self.today_event = Event.objects.create(
            title="today_event", owner=self.user, date=FIXED_TODAY
        )
        self.upcoming_event = Event.objects.create(
            title="upcoming_event", owner=self.user, date=FIXED_TOMORROW
        )
        self.past_event = Event.objects.create(
            title="past_event", owner=self.user, date=FIXED_YESTERDAY
        )
        Event.objects.create(title="other_event", owner=other, date=FIXED_TODAY)

        self.active_goal = Goal.objects.create(
            title="active_goal", owner=self.user, progress=50
        )
        self.completed_goal = Goal.objects.create(
            title="completed_goal", owner=self.user, progress=100
        )
        Goal.objects.create(title="other_goal", owner=other, progress=50)

        _start_date_patches(self)

    def _get(self):
        return self.client.get(reverse("dashboard:index"))

    def test_all_five_context_keys_present(self):
        ctx = self._get().context
        for key in (
            "overdue_tasks",
            "pending_tasks",
            "today_events",
            "upcoming_events",
            "active_goals",
        ):
            self.assertIn(key, ctx)

    def test_overdue_tasks_includes_only_pending_with_past_due_date(self):
        ctx = self._get().context
        qs = ctx["overdue_tasks"]
        self.assertIn(self.overdue, qs)
        self.assertNotIn(self.pending_due_today, qs)
        self.assertNotIn(self.pending_future, qs)
        self.assertNotIn(self.pending_no_due, qs)
        self.assertNotIn(self.completed, qs)

    def test_pending_tasks_includes_pending_not_overdue(self):
        ctx = self._get().context
        qs = ctx["pending_tasks"]
        self.assertIn(self.pending_due_today, qs)
        self.assertIn(self.pending_future, qs)
        self.assertIn(self.pending_no_due, qs)
        self.assertNotIn(self.overdue, qs)
        self.assertNotIn(self.completed, qs)

    def test_today_events_includes_only_todays_events(self):
        ctx = self._get().context
        qs = ctx["today_events"]
        self.assertIn(self.today_event, qs)
        self.assertNotIn(self.upcoming_event, qs)
        self.assertNotIn(self.past_event, qs)

    def test_upcoming_events_includes_only_future_events(self):
        ctx = self._get().context
        qs = ctx["upcoming_events"]
        self.assertIn(self.upcoming_event, qs)
        self.assertNotIn(self.today_event, qs)
        self.assertNotIn(self.past_event, qs)

    def test_active_goals_includes_only_incomplete_goals(self):
        ctx = self._get().context
        qs = ctx["active_goals"]
        self.assertIn(self.active_goal, qs)
        self.assertNotIn(self.completed_goal, qs)

    def test_no_block_contains_other_users_data(self):
        # Isolamento por owner validado no contexto do Dashboard completo.
        # DashboardOwnerIsolationTest (T8.5) cobre o caso dedicado.
        ctx = self._get().context
        self.assertEqual(ctx["overdue_tasks"].count(), 1)
        self.assertEqual(ctx["pending_tasks"].count(), 3)
        self.assertEqual(ctx["today_events"].count(), 1)
        self.assertEqual(ctx["upcoming_events"].count(), 1)
        self.assertEqual(ctx["active_goals"].count(), 1)


class DashboardEmptyContextTest(SibylTestCase):
    def setUp(self):
        self.user = self.make_user()
        self.login(self.user)
        _start_date_patches(self)

    def test_all_five_blocks_exist_and_are_empty(self):
        ctx = self.client.get(reverse("dashboard:index")).context
        self.assertFalse(ctx["overdue_tasks"].exists())
        self.assertFalse(ctx["pending_tasks"].exists())
        self.assertFalse(ctx["today_events"].exists())
        self.assertFalse(ctx["upcoming_events"].exists())
        self.assertFalse(ctx["active_goals"].exists())
