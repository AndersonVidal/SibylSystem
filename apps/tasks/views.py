from django.shortcuts import render


def index(request):
    return render(request, "tasks/index.html", {"active_nav": "tasks"})
