from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from comments.models import Comment
from core.views import form_errors_iter
from posts.models import Post

from . import forms

MESSAGE_WELCOME = _("Welcome back!")
MESSAGE_UPDATED = _("Updated successfully")
USER_SETTINGS_URL = reverse_lazy("settings")


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

        errors = list(form_errors_iter(form))
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

        errors = list(form_errors_iter(form))
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
        typee = request.GET.get("type", None)
        page = request.GET.get("page", 1)

        try:
            user = get_user_model().objects.get(nickname=nickname)
            if typee == "comment":
                objects = Comment.objects.filter(writer=user).order_by("-id")
                per_page = 15
            else:
                objects = Post.objects.filter(writer=user).order_by("-id")
                per_page = 5

            paginator = Paginator(objects, per_page)

            try:
                paginated_objs = paginator.page(page)
            except PageNotAnInteger:
                paginated_objs = paginator.page(1)
            except EmptyPage:
                paginated_objs = paginator.page(paginator.num_pages)

            return render(
                request,
                "users/detail.html",
                {"user_obj": user, "paginated_objs": paginated_objs, "type": typee},
            )
        except get_user_model().DoesNotExist:
            return redirect("home")

    return HttpResponseBadRequest()


@login_required
def settings_view(request):
    return render(request, "users/settings.html", status=200)


@login_required
def update_email_view(request):
    """Update user's email view"""

    errors = []

    if request.method == "POST":
        form = forms.UpdateEmailForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, MESSAGE_UPDATED)
            return redirect(USER_SETTINGS_URL)

        errors = list(form_errors_iter(form))
    elif request.method == "GET":
        form = forms.UpdateEmailForm(user=request.user)

    return render(
        request,
        "users/update.html",
        {"form": form, "errors": errors, "cta": "email"},
        status=200,
    )


@login_required
def update_nickname_view(request):
    """Update user's nickname view"""

    errors = []

    if request.method == "POST":
        form = forms.UpdateNicknameForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, MESSAGE_UPDATED)
            return redirect(USER_SETTINGS_URL)

        errors = list(form_errors_iter(form))
    elif request.method == "GET":
        form = forms.UpdateNicknameForm(user=request.user)

    return render(
        request,
        "users/update.html",
        {"form": form, "errors": errors, "cta": "nickname"},
        status=200,
    )


@login_required
def update_password_view(request):
    """Update user's password view"""

    errors = []
    if request.method == "POST":
        form = forms.UpdatePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, MESSAGE_UPDATED)
            return redirect(USER_SETTINGS_URL)
        errors = list(form_errors_iter(form))
    elif request.method == "GET":
        form = forms.UpdatePasswordForm(user=request.user)
    return render(
        request,
        "users/update.html",
        {"form": form, "errors": errors, "cta": "password"},
        status=200,
    )


@login_required
def update_avatar_view(request):
    """Update user's avatar view"""

    errors = []

    if request.method == "POST":
        request.user.avatar = request.FILES.get("new_avatar", None)
        request.user.save()
        messages.success(request, MESSAGE_UPDATED)
        return redirect(USER_SETTINGS_URL)

    form = forms.UpdateAvatarForm()

    return render(
        request,
        "users/update.html",
        {"form": form, "errors": errors, "cta": "avatar"},
        status=200,
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
        errors = list(form_errors_iter(form))

    elif request.method == "GET":
        form = forms.DeleteAccountForm(user=request.user)
    return render(
        request,
        "users/delete.html",
        {"form": form, "errors": errors, "cta": "account"},
        status=200,
    )
