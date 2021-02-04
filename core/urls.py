from django.urls import path

from . import views
from users.views import sign_up, log_in, log_out, user_settings, update_email

settings_router = [
    path("settings/", user_settings, name="settings"),
    path("settings/password", update_email, name="update-password"),
    # path("settings/nickname", user_settings, name="update-nickname"),
    # path("settings/email", user_settings, name="update-email"),
]

urlpatterns = [
    path("", views.home_view, name="home"),
    path("signup/", sign_up, name="sign-up"),
    path("login/", log_in, name="login"),
    path("logout/", log_out, name="logout"),
] + settings_router
