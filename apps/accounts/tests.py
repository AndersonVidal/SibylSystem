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
