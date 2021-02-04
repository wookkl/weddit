from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, get_user_model, login, logout

from . import forms

MESSAGE_WELCOME = _("Welcome back!")
MESSAGE_UPDATED = _("Updated successfully")


def sign_up(request):
    """Create user view"""
    if request.method == "POST":
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, MESSAGE_WELCOME)
            return redirect(reverse("home"))
        for key in form.errors.as_data().keys():
            for error in form.errors.as_data()[key]:
                messages.error(request, error.message)
    elif request.method == "GET":
        form = forms.CustomUserCreationForm()
    return render(request, "core/signup.html", {"form": form}, status=200)


def log_in(request):
    """Login user view"""
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, MESSAGE_WELCOME)
                return redirect(reverse("home"))
        for key in form.errors.as_data().keys():
            for error in form.errors.as_data()[key]:
                messages.error(request, error.message)
    elif request.method == "GET":
        form = forms.LoginForm()
    return render(request, "core/login.html", {"form": form}, status=200)


@login_required(login_url=reverse_lazy("login"))
def log_out(request):
    logout(request)
    return redirect(reverse("home"))


@require_http_methods(["GET"])
def user_detail(request, nickname):
    if request.method == "GET":
        try:
            user = get_user_model().objects.get(nickname=nickname)
            return render(request, "users/detail.html", {"user_obj": user})
        except get_user_model().DoesNotExist:
            return redirect("home")


@login_required(login_url=reverse_lazy("login"))
def user_settings(request):
    return render(request, "users/settings.html", status=200)


@login_required(login_url=reverse_lazy("login"))
def update_email(request):
    if request.method == "POST":
        form = forms.UpdateEmailForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, MESSAGE_UPDATED)
            return redirect(reverse("settings"))
        for key in form.errors.as_data().keys():
            for error in form.errors.as_data()[key]:
                messages.error(request, error.message)
    elif request.method == "GET":
        form = forms.UpdateEmailForm(user=request.user)
    return render(request, "users/update.html", {"form": form}, status=200)


@login_required(login_url=reverse_lazy("login"))
def update_nickname(request):
    if request.method == "POST":
        form = forms.UpdateNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, MESSAGE_UPDATED)
            return redirect(reverse("settings"))
        for key in form.errors.as_data().keys():
            for error in form.errors.as_data()[key]:
                messages.error(request, error.message)
    elif request.method == "GET":
        form = forms.UpdateNicknameForm(user=request.user)
    return render(request, "users/update.html", {"form": form}, status=200)
