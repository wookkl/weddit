from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from communities.models import Community
from posts.models import Post


@require_http_methods(["GET"])
def home_view(request):
    """Home view"""
    posts = Post.objects.all()
    page = request.GET.get("page", 1)
    paginator = Paginator(posts, 20)
    try:
        paginated_posts = paginator.page(page)
    except PageNotAnInteger:
        paginated_posts = paginator.page(1)
    except EmptyPage:
        paginated_posts = paginator.page(paginator.num_pages)

    community_obj = Community.objects.all().order_by("-pk")[:10]

    return render(
        request,
        "home.html",
        {"communities": community_obj, "posts": paginated_posts},
    )
