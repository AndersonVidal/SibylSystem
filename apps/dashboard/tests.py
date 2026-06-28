import datetime

from django.urls import reverse
from django.utils import timezone

from apps.events.models import Event
from apps.goals.models import Goal
from apps.tasks.models import Task
from tests.base import SibylTestCase


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
