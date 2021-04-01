from django.urls import path

from .views import vote_toggle_view

app_name = "votes"

urlpatterns = [
    path("toggle/", vote_toggle_view, name="toggle"),
]
