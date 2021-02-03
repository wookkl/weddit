from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import login
from django.utils.translation import gettext as _

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
