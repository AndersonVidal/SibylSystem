import shutil
import tempfile
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from django.conf import settings as django_settings
from django.core.management import call_command

from tests.base import SibylTestCase

PROTECTED_ROUTES = ["/", "/tasks/", "/events/", "/goals/"]


class LoginPageTest(SibylTestCase):
    def test_get_returns_200_with_form(self):
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)


class LoginTest(SibylTestCase):
    def setUp(self):
        self.user = self.make_user()

    def test_valid_credentials_redirect_to_home_and_authenticate(self):
        response = self.client.post(
            "/accounts/login/",
            data={"username": "testuser", "password": "testpass123"},
        )
        self.assertRedirects(response, "/")
        self.assertIn("_auth_user_id", self.client.session)

    def test_invalid_credentials_return_200_with_errors_unauthenticated(self):
        response = self.client.post(
            "/accounts/login/",
            data={"username": "testuser", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertNotIn("_auth_user_id", self.client.session)


class LogoutTest(SibylTestCase):
    def setUp(self):
        self.user = self.make_user()
        self.login(self.user)

    def test_post_redirects_to_login_and_unauthenticates(self):
        response = self.client.post("/accounts/logout/")
        self.assertRedirects(response, "/accounts/login/")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_get_returns_405(self):
        response = self.client.get("/accounts/logout/")
        self.assertEqual(response.status_code, 405)


class ProtectedRoutesTest(SibylTestCase):
    def test_unauthenticated_redirects_to_login_with_next(self):
        for route in PROTECTED_ROUTES:
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertRedirects(
                    response,
                    f"/accounts/login/?next={route}",
                    fetch_redirect_response=False,
                )

    def test_authenticated_returns_200(self):
        self.login(self.make_user())
        for route in PROTECTED_ROUTES:
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertEqual(response.status_code, 200)


class NextParamFlowTest(SibylTestCase):
    def setUp(self):
        self.user = self.make_user()

    def test_next_param_redirects_to_original_route_after_login(self):
        response = self.client.get("/tasks/")
        self.assertRedirects(
            response,
            "/accounts/login/?next=/tasks/",
            fetch_redirect_response=False,
        )
        response = self.client.post(
            "/accounts/login/?next=/tasks/",
            data={"username": "testuser", "password": "testpass123"},
        )
        self.assertRedirects(response, "/tasks/", fetch_redirect_response=False)
        response = self.client.get("/tasks/")
        self.assertEqual(response.status_code, 200)


# ---------------------------------------------------------------------------
# Backup command
# ---------------------------------------------------------------------------

FIXED_TIMESTAMP = "20260702-120000"
FIXED_BACKUP_NAME = f"database-{FIXED_TIMESTAMP}.sqlite3"


class BackupCommandTestBase(SibylTestCase):
    """Configura diretórios temporários e patches de settings para os testes de backup."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.backup_dir = self.tmp / "backups"
        self.backup_dir.mkdir()
        self.db_path = self.tmp / "database.sqlite3"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _call_backup(self):
        out = StringIO()
        db_patch = patch.object(
            django_settings,
            "DATABASES",
            {"default": {"NAME": self.db_path, "ENGINE": "django.db.backends.sqlite3"}},
        )
        dir_patch = patch.object(django_settings, "DATA_DIR", self.tmp)
        dt_patch = patch(
            "apps.accounts.management.commands.backup.datetime",
        )
        with db_patch, dir_patch, dt_patch as mock_dt:
            mock_dt.now.return_value.strftime.return_value = FIXED_TIMESTAMP
            call_command("backup", stdout=out)
        return out.getvalue()


class BackupCommandWithDatabaseTest(BackupCommandTestBase):
    def setUp(self):
        super().setUp()
        self.db_path.write_bytes(b"sqlite")

    def test_backup_file_is_created(self):
        self._call_backup()
        self.assertTrue((self.backup_dir / FIXED_BACKUP_NAME).exists())

    def test_backup_file_has_correct_name(self):
        self._call_backup()
        backups = list(self.backup_dir.glob("database-*.sqlite3"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].name, FIXED_BACKUP_NAME)

    def test_output_contains_backup_path(self):
        out = self._call_backup()
        self.assertIn(FIXED_BACKUP_NAME, out)

    def test_backup_file_content_matches_source(self):
        self._call_backup()
        content = (self.backup_dir / FIXED_BACKUP_NAME).read_bytes()
        self.assertEqual(content, b"sqlite")


class BackupRetentionTest(BackupCommandTestBase):
    def setUp(self):
        super().setUp()
        self.db_path.write_bytes(b"sqlite")

    def _seed_backups(self, count: int):
        for i in range(count):
            (self.backup_dir / f"database-2026010{i:01d}-000000.sqlite3").write_bytes(
                b"old"
            )

    def test_eleven_backups_leaves_ten(self):
        self._seed_backups(10)
        self._call_backup()
        remaining = list(self.backup_dir.glob("database-*.sqlite3"))
        self.assertEqual(len(remaining), 10)

    def test_oldest_backup_is_removed(self):
        self._seed_backups(10)
        self._call_backup()
        names = sorted(b.name for b in self.backup_dir.glob("database-*.sqlite3"))
        # O mais antigo (20260100-...) não deve mais existir
        self.assertFalse(any(n.startswith("database-20260100") for n in names))

    def test_newest_backup_is_preserved(self):
        self._seed_backups(10)
        self._call_backup()
        self.assertTrue((self.backup_dir / FIXED_BACKUP_NAME).exists())

    def test_exactly_ten_backups_no_removal(self):
        self._seed_backups(9)
        self._call_backup()
        remaining = list(self.backup_dir.glob("database-*.sqlite3"))
        self.assertEqual(len(remaining), 10)


class BackupCommandWithoutDatabaseTest(BackupCommandTestBase):
    def test_missing_db_does_not_raise(self):
        try:
            self._call_backup()
        except Exception as exc:
            self.fail(f"Comando levantou exceção inesperada: {exc}")

    def test_missing_db_outputs_warning(self):
        out = self._call_backup()
        self.assertIn("não encontrado", out.lower())
