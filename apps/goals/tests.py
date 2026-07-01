import datetime

from django.urls import reverse

from apps.goals.models import Goal
from tests.base import SibylTestCase


class GoalQuerySetActiveTest(SibylTestCase):
    def setUp(self):
        self.user = self.make_user()

    def _goal(self, progress, **kwargs):
        return Goal.objects.create(
            title="g", owner=self.user, progress=progress, **kwargs
        )

    def _qs(self):
        return Goal.objects.filter(owner=self.user).active()

    def test_progress_zero_returned(self):
        self._goal(0)
        self.assertEqual(self._qs().count(), 1)

    def test_progress_fifty_returned(self):
        self._goal(50)
        self.assertEqual(self._qs().count(), 1)

    def test_progress_99_returned(self):
        self._goal(99)
        self.assertEqual(self._qs().count(), 1)

    def test_progress_100_not_returned(self):
        self._goal(100)
        self.assertFalse(self._qs().exists())

    def test_other_user_goal_not_returned(self):
        other = self.make_user(username="other")
        Goal.objects.create(title="g", owner=other, progress=50)
        self.assertFalse(self._qs().exists())


class GoalEditTest(SibylTestCase):
    def setUp(self):
        self.user = self.make_user()
        self.login(self.user)
        self.goal = Goal.objects.create(
            title="Original",
            owner=self.user,
            progress=30,
            target_date=datetime.date(2026, 12, 31),
        )

    def test_get_returns_200(self):
        response = self.client.get(reverse("goals:edit", args=[self.goal.pk]))
        self.assertEqual(response.status_code, 200)

    def test_get_form_prefilled_with_current_data(self):
        response = self.client.get(reverse("goals:edit", args=[self.goal.pk]))
        self.assertEqual(response.context["form"]["title"].value(), "Original")
        self.assertEqual(response.context["form"]["progress"].value(), 30)
        self.assertEqual(
            response.context["form"]["target_date"].value(),
            datetime.date(2026, 12, 31),
        )

    def test_post_valid_updates_title(self):
        self.client.post(
            reverse("goals:edit", args=[self.goal.pk]),
            {"title": "Atualizado", "progress": 30, "target_date": ""},
        )
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.title, "Atualizado")

    def test_post_valid_updates_progress(self):
        self.client.post(
            reverse("goals:edit", args=[self.goal.pk]),
            {"title": "Original", "progress": 75, "target_date": ""},
        )
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.progress, 75)

    def test_post_valid_updates_target_date(self):
        self.client.post(
            reverse("goals:edit", args=[self.goal.pk]),
            {"title": "Original", "progress": 30, "target_date": "2027-06-01"},
        )
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.target_date, datetime.date(2027, 6, 1))

    def test_post_valid_clears_target_date(self):
        self.client.post(
            reverse("goals:edit", args=[self.goal.pk]),
            {"title": "Original", "progress": 30, "target_date": ""},
        )
        self.goal.refresh_from_db()
        self.assertIsNone(self.goal.target_date)

    def test_post_valid_redirects_to_index(self):
        response = self.client.post(
            reverse("goals:edit", args=[self.goal.pk]),
            {"title": "Atualizado", "progress": 50, "target_date": ""},
        )
        self.assertRedirects(response, reverse("goals:index"))

    def test_post_empty_title_returns_200(self):
        response = self.client.post(
            reverse("goals:edit", args=[self.goal.pk]),
            {"title": "", "progress": 30, "target_date": ""},
        )
        self.assertEqual(response.status_code, 200)

    def test_post_progress_below_zero_returns_200(self):
        response = self.client.post(
            reverse("goals:edit", args=[self.goal.pk]),
            {"title": "Original", "progress": -1, "target_date": ""},
        )
        self.assertEqual(response.status_code, 200)

    def test_post_progress_above_100_returns_200(self):
        response = self.client.post(
            reverse("goals:edit", args=[self.goal.pk]),
            {"title": "Original", "progress": 101, "target_date": ""},
        )
        self.assertEqual(response.status_code, 200)

    def test_post_invalid_does_not_save(self):
        self.client.post(
            reverse("goals:edit", args=[self.goal.pk]),
            {"title": "", "progress": 30, "target_date": ""},
        )
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.title, "Original")
        self.assertEqual(self.goal.progress, 30)

    def test_get_other_users_goal_returns_404(self):
        other = self.make_user(username="other")
        other_goal = Goal.objects.create(title="Other", owner=other, progress=50)
        response = self.client.get(reverse("goals:edit", args=[other_goal.pk]))
        self.assertEqual(response.status_code, 404)

    def test_post_other_users_goal_returns_404(self):
        other = self.make_user(username="other")
        other_goal = Goal.objects.create(title="Other", owner=other, progress=50)
        response = self.client.post(
            reverse("goals:edit", args=[other_goal.pk]),
            {"title": "Hacked", "progress": 100, "target_date": ""},
        )
        self.assertEqual(response.status_code, 404)
        other_goal.refresh_from_db()
        self.assertEqual(other_goal.title, "Other")

    def test_edit_does_not_change_owner(self):
        self.client.post(
            reverse("goals:edit", args=[self.goal.pk]),
            {"title": "Atualizado", "progress": 50, "target_date": ""},
        )
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.owner, self.user)
