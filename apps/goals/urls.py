from django.urls import path

from . import views

app_name = "goals"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/progress/", views.update_progress, name="update_progress"),
]
