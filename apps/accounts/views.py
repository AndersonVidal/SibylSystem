from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import redirect, render

from apps.accounts.forms import InitialUserRegistrationForm

User = get_user_model()


class SibylLoginView(LoginView):
    template_name = "accounts/login.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user_exists = User.objects.exists()
        ctx["user_exists"] = user_exists
        if not user_exists:
            ctx["register_form"] = InitialUserRegistrationForm()
        return ctx


def register(request):
    if User.objects.exists():
        raise Http404

    if request.method == "POST":
        form = InitialUserRegistrationForm(request.POST)
        if form.is_valid():
            if User.objects.exists():
                raise Http404
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                password=data["password"],
                is_staff=True,
                is_superuser=True,
            )
            login(request, user)
            return redirect("/")

        return render(
            request,
            "accounts/login.html",
            {
                "form": AuthenticationForm(),
                "register_form": form,
                "show_register_modal": True,
                "user_exists": False,
            },
        )

    # GET — render login page with modal open
    return render(
        request,
        "accounts/login.html",
        {
            "form": AuthenticationForm(),
            "register_form": InitialUserRegistrationForm(),
            "show_register_modal": True,
            "user_exists": False,
        },
    )
