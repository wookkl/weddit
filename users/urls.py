from django.urls import path

from . import views

app_name = "user"


urlpatterns = [
    path("<str:nickname>/", views.user_detail_view, name="detail"),
]
