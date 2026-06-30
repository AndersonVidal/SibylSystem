from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import redirect, render

from apps.events.forms import EventForm
from apps.events.models import Event


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
    events = Event.objects.filter(owner=request.user).order_by(
        "date", F("time").asc(nulls_last=True), "title"
    )
    return render(
        request,
        "events/index.html",
        {"active_nav": "events", "form": form, "events": events},
    )
