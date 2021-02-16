from django.urls import path

from .views import subscription_toggle_view

app_name = "subscriptions"

urlpatterns = [
    path("toggle/", subscription_toggle_view, name="toggle"),
]
