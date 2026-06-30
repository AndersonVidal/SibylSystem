from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render

from apps.events.models import Event
from apps.goals.models import Goal
from apps.tasks.models import Task


@login_required
def index(request):
    overdue_tasks = (
        Task.objects.filter(owner=request.user)
        .overdue()
        .order_by(F("due_date").asc(nulls_last=True), "title")
    )
    pending_tasks = (
        Task.objects.filter(owner=request.user)
        .pending_not_overdue()
        .order_by(F("due_date").asc(nulls_last=True), "title")
    )
    today_events = (
        Event.objects.filter(owner=request.user)
        .today()
        .order_by(F("time").asc(nulls_last=True), "title")
    )
    upcoming_events = (
        Event.objects.filter(owner=request.user)
        .upcoming()
        .order_by("date", F("time").asc(nulls_last=True), "title")
    )
    active_goals = (
        Goal.objects.filter(owner=request.user)
        .active()
        .order_by("progress", F("target_date").asc(nulls_last=True), "title")
    )
    return render(
        request,
        "dashboard/index.html",
        {
            "active_nav": "dashboard",
            "overdue_tasks": overdue_tasks,
            "pending_tasks": pending_tasks,
            "today_events": today_events,
            "upcoming_events": upcoming_events,
            "active_goals": active_goals,
        },
    )
