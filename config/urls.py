"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

admin_urls = os.environ.get("ADMIN_URL", "admin")

urlpatterns = [
    path(f"{admin_urls}/", admin.site.urls),
    path("", include("core.urls")),
    path("user/", include("users.urls", namespace="user")),
    path("communities/", include("communities.urls", namespace="communities")),
    path("posts/", include("posts.urls", namespace="posts")),
    path("subscriptions/", include("subscriptions.urls", namespace="subscriptions")),
    path("comments/", include("comments.urls", namespace="comments")),
    path("votes/", include("votes.urls", namespace="votes")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
