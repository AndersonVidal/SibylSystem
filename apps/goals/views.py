from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.goals.forms import GoalForm, GoalProgressForm
from apps.goals.models import Goal


@login_required
def index(request):
    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.owner = request.user
            goal.save()
            return redirect("goals:index")
    else:
        form = GoalForm()
    goals = Goal.objects.filter(owner=request.user).order_by(
        "progress", F("target_date").asc(nulls_last=True), "title"
    )
    return render(
        request,
        "goals/index.html",
        {"active_nav": "goals", "form": form, "goals": goals},
    )


@login_required
def edit(request, pk):
    goal = get_object_or_404(Goal, pk=pk, owner=request.user)
    if request.method == "POST":
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect("goals:index")
    else:
        form = GoalForm(instance=goal)
    return render(
        request,
        "goals/edit.html",
        {"active_nav": "goals", "form": form, "goal": goal},
    )


@login_required
@require_POST
def update_progress(request, pk):
    goal = get_object_or_404(Goal, pk=pk, owner=request.user)
    form = GoalProgressForm(request.POST, instance=goal)
    if form.is_valid():
        form.save()
    return redirect("goals:index")
