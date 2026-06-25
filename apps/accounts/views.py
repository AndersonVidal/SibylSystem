from django.contrib.auth.views import LoginView


class SibylLoginView(LoginView):
    template_name = "accounts/login.html"
