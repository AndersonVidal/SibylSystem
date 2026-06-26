from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import redirect, render

from apps.tasks.forms import TaskForm
from apps.tasks.models import Task


@login_required
def index(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect("tasks:index")
    else:
        form = TaskForm()
    tasks = Task.objects.filter(owner=request.user).order_by(
        F("due_date").asc(nulls_last=True), "title"
    )
    return render(
        request,
        "tasks/index.html",
        {"active_nav": "tasks", "form": form, "tasks": tasks},
    )
