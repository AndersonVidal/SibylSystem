from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

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


@login_required
def edit(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("tasks:index")
    else:
        form = TaskForm(instance=task)
    return render(
        request, "tasks/edit.html", {"active_nav": "tasks", "form": form, "task": task}
    )


@login_required
@require_POST
def complete(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    task.status = Task.Status.COMPLETED
    task.save()
    return redirect("tasks:index")
