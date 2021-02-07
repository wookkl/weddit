from django.urls import path

from . import views

app_name = "communities"

urlpatterns = [
    path("", views.CommunityListView.as_view(), name="list"),
    path("create/", views.CommunityCreateView.as_view(), name="create"),
]
