from django.urls import path

from .views import CommunityCreateView, CommunityDetailView, CommunityListView

app_name = "communities"

urlpatterns = [
    path("", CommunityListView.as_view(), name="list"),
    path("create/", CommunityCreateView.as_view(), name="create"),
    path("<slug:slug>", CommunityDetailView.as_view(), name="detail"),
]
