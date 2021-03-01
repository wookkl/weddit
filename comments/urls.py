from django.urls import path

from .views import CreateCommentView, comment_delete_view

app_name = "comments"

urlpatterns = [
    path("create/", CreateCommentView.as_view(), name="create"),
    path("delete/<int:pk>/", comment_delete_view, name="delete"),
]
