from django.urls import path

from . import views
from users.views import sign_up_view, log_in, log_out

urlpatterns = [
    path("", views.home_view, name="home"),
    path("signup/", sign_up_view, name="sign-up"),
    path("login/", log_in, name="login"),
    path("logout/", log_out, name="logout"),
]
