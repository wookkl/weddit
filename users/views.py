from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from . import forms


def sign_up_view(request):
    """Create user view"""
    if request.method == "POST":
        form = forms.CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _("Account created successfully"))
            return redirect(reverse("home"))

        for key in form.errors.as_data().keys():
            for error in form.errors.as_data()[key]:
                messages.error(request, error.message)

    elif request.method == "GET":
        form = forms.CustomUserCreationForm()

    return render(request, "core/signup.html", {"form": form})


@require_http_methods(["GET"])
def user_detail(request, nickname):
    if request.method == "GET":
        try:
            user = get_user_model().objects.get(nickname=nickname)
            return render(request, "users/detail.html", {"user_obj": user})

        except get_user_model().DoesNotExist:
            return redirect("home")
