from django.urls import path

from . import views
from users.views import sign_up_view

urlpatterns = [
    path("signup/", sign_up_view, name="sign-up"),
    path("", views.home_view, name="home"),
]
