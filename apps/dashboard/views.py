from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.tasks.models import Task


@login_required
def index(request):
    overdue_tasks = Task.objects.filter(owner=request.user).overdue()
    return render(
        request,
        "dashboard/index.html",
        {"active_nav": "dashboard", "overdue_tasks": overdue_tasks},
    )
