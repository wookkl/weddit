from django.urls import path

from . import views
from users import views as user_views

settings_router = [
    path("settings/", user_views.user_settings, name="settings"),
    path("settings/email/", user_views.update_email, name="update-email"),
    path("settings/nickname/", user_views.update_nickname, name="update-nickname"),
    path("settings/password/", user_views.update_password, name="update-password"),
    path("settings/delete-account/", user_views.delete_account, name="delete-account"),
]
urlpatterns = [
    path("", views.home_view, name="home"),
    path("signup/", user_views.sign_up, name="sign-up"),
    path("login/", user_views.log_in, name="login"),
    path("logout/", user_views.log_out, name="logout"),
] + settings_router
