from django.urls import path

from users import views as user_views

from . import views

settings_router = [
    path("settings/", user_views.settings_view, name="settings"),
    path("settings/email/", user_views.update_email_view, name="update-email"),
    path("settings/nickname/", user_views.update_nickname_view, name="update-nickname"),
    path("settings/password/", user_views.update_password_view, name="update-password"),
    path("settings/avatar/", user_views.update_avatar_view, name="update-avatar"),
    path("settings/delete/", user_views.user_delete_view, name="delete-account"),
]

urlpatterns = [
    path("", views.home_view, name="home"),
    path("signup/", user_views.signup_view, name="sign-up"),
    path("login/", user_views.login_view, name="login"),
    path("logout/", user_views.logout_view, name="logout"),
    path("search/", views.search_view, name="search"),
] + settings_router
