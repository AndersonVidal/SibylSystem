from django.urls import path

from apps.accounts.views import SibylLoginView

app_name = "accounts"

urlpatterns = [
    path("login/", SibylLoginView.as_view(), name="login"),
]
