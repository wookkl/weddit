from django.urls import path
from users import views

app_name = "user"


urlpatterns = [
    path("<str:nickname>/", views.detail_view, name="detail"),
]
