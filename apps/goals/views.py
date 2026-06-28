from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.goals.forms import GoalForm


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
    return render(request, "goals/index.html", {"active_nav": "goals", "form": form})
