from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.events.models import Event
from apps.tasks.models import Task


@login_required
def index(request):
    overdue_tasks = Task.objects.filter(owner=request.user).overdue()
    pending_tasks = Task.objects.filter(owner=request.user).pending_not_overdue()
    today_events = (
        Event.objects.filter(owner=request.user).today().order_by("time", "title")
    )
    return render(
        request,
        "dashboard/index.html",
        {
            "active_nav": "dashboard",
            "overdue_tasks": overdue_tasks,
            "pending_tasks": pending_tasks,
            "today_events": today_events,
        },
    )
