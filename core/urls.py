from django.urls import path

from . import views
from users import views as user_views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("signup/", user_views.sign_up, name="sign-up"),
    path("login/", user_views.log_in, name="login"),
    path("logout/", user_views.log_out, name="logout"),
]
