from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("events/", include("apps.events.urls")),
    path("tasks/", include("apps.tasks.urls")),
    path("goals/", include("apps.goals.urls")),
    path("", include("apps.dashboard.urls")),
]
