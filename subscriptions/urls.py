from django.urls import path

from .views import SubscriptionToggleView

app_name = "subscriptions"

urlpatterns = [
    path("toggle/", SubscriptionToggleView.as_view(), name="toggle"),
]
