from django.urls import path

from .views import (
    PostListView,
    PostCreateView,
    PostDetailView,
    post_delete_view,
    PostUpdateView,
)

app_name = "posts"

urlpatterns = [
    path("", PostListView.as_view(), name="list"),
    path("create/", PostCreateView.as_view(), name="create"),
    path("<int:pk>/", PostDetailView.as_view(), name="detail"),
    path("delete/<int:pk>/", post_delete_view, name="delete"),
    path("update/<int:pk>/", PostUpdateView.as_view(), name="update"),
]
