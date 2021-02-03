from django.urls import path
from .views import user_detail

app_name = "user"

urlpatterns = [
    path("<str:nickname>/", user_detail, name="detail"),
]
