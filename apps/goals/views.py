from django.shortcuts import render


def index(request):
    return render(request, "goals/index.html", {"active_nav": "goals"})
