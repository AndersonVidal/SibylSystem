from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.tasks.forms import TaskForm


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
    return render(request, "tasks/index.html", {"active_nav": "tasks", "form": form})
