from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import redirect, render

from apps.goals.forms import GoalForm
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
