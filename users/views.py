from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.conf import settings
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from posts.models import Post
from . import forms

MESSAGE_WELCOME = _("Welcome back!")
MESSAGE_UPDATED = _("Updated successfully")
USER_SETTINGS_URL = reverse_lazy("settings")


def get_errors(form):
    errors = []
    for key in form.errors.as_data().keys():
        for error in form.errors.as_data()[key]:
            errors.append(error.message)
    return errors


# VIEWS
def signup_view(request):
    """Create user view"""

    errors = []
    if request.method == "POST":
        form = forms.CustomUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, MESSAGE_WELCOME)
            return redirect(settings.LOGIN_REDIRECT_URL)
        errors = get_errors(form)
    elif request.method == "GET":
        form = forms.CustomUserCreateForm()
    return render(
        request, "core/signup.html", {"form": form, "errors": errors}, status=200
    )


def login_view(request):
    """Login user view"""

    errors = []
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, MESSAGE_WELCOME)
                return redirect(settings.LOGIN_REDIRECT_URL)
        errors = get_errors(form)
    elif request.method == "GET":
        form = forms.LoginForm()
    return render(
        request, "core/login.html", {"form": form, "errors": errors}, status=200
    )


@login_required
def logout_view(request):
    """Log out view"""

    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


@require_http_methods(["GET"])
def user_detail_view(request, nickname):
    """User detail view"""
    if request.method == "GET":
        try:
            user = get_user_model().objects.get(nickname=nickname)
            posts = Post.objects.filter(writer=user).order_by("-id")
            page = request.GET.get("page", 1)
            paginator = Paginator(posts, 5)
            try:
                paginated_posts = paginator.page(page)
            except PageNotAnInteger:
                paginated_posts = paginator.page(1)
            except EmptyPage:
                paginated_posts = paginator.page(paginator.num_pages)

            return render(
                request,
                "users/detail.html",
                {"user_obj": user, "post_obj": paginated_posts},
            )
        except get_user_model().DoesNotExist:
            return redirect("home")


@login_required
def settings_view(request):
    return render(request, "users/settings.html", status=200)


@login_required
def update_email_view(request):
    errors = []
    if request.method == "POST":
        form = forms.UpdateEmailForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, MESSAGE_UPDATED)
            return redirect(USER_SETTINGS_URL)
        errors = get_errors(form)
    elif request.method == "GET":
        form = forms.UpdateEmailForm(user=request.user)
    return render(
        request, "users/update.html", {"form": form, "errors": errors}, status=200
    )


@login_required
def update_nickname_view(request):
    errors = []
    if request.method == "POST":
        form = forms.UpdateNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, MESSAGE_UPDATED)
            return redirect(USER_SETTINGS_URL)
        errors = get_errors(form)
    elif request.method == "GET":
        form = forms.UpdateNicknameForm(user=request.user)
    return render(
        request, "users/update.html", {"form": form, "errors": errors}, status=200
    )


@login_required
def update_password_view(request):
    errors = []
    if request.method == "POST":
        form = forms.UpdatePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, MESSAGE_UPDATED)
            return redirect(USER_SETTINGS_URL)
        errors = get_errors(form)
    elif request.method == "GET":
        form = forms.UpdatePasswordForm(user=request.user)
    return render(
        request, "users/update.html", {"form": form, "errors": errors}, status=200
    )


@login_required
def update_avatar_view(request):
    errors = []
    if request.method == "POST":
        request.user.avatar = request.FILES.get("new_avatar", None)
        request.user.save()
        messages.success(request, MESSAGE_UPDATED)
        return redirect(USER_SETTINGS_URL)
    form = forms.UpdateAvatarForm()
    return render(
        request, "users/update.html", {"form": form, "errors": errors}, status=200
    )


@login_required
def user_delete_view(request):
    errors = []
    if request.method == "POST":
        form = forms.DeleteAccountForm(request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            logout(request)
            user.delete()
            messages.success(request, _("Account successfully deleted"))
            return redirect(settings.LOGOUT_REDIRECT_URL)
        errors = get_errors(form)
    elif request.method == "GET":
        form = forms.DeleteAccountForm(user=request.user)
    return render(
        request, "users/delete.html", {"form": form, "errors": errors}, status=200
    )
