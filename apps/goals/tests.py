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
