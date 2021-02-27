from django.urls import path

from .views import CreateCommentView

app_name = "comments"

urlpatterns = [
    path("create/", CreateCommentView.as_view(), name="create"),
]
