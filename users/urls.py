from django.urls import path
from users import views

app_name = "user"

settings_router = [
    path("settings/", views.user_settings, name="settings"),
    path("settings/email/", views.update_email, name="update-email"),
    path("settings/nickname/", views.update_nickname, name="update-nickname"),
    path("settings/password/", views.update_password, name="update-password"),
    path("settings/delete/", views.delete_account, name="delete-account"),
]
urlpatterns = [
    path("<str:nickname>/", views.user_detail, name="detail"),
] + settings_router
