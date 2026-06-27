from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.events.forms import EventForm


@login_required
def index(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            event.save()
            return redirect("events:index")
    else:
        form = EventForm()
    return render(request, "events/index.html", {"active_nav": "events", "form": form})
