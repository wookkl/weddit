from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from communities.models import Community
from posts.models import Post


def get_form_errors(form):
    errors = []
    for key in form.errors.as_data().keys():
        for error in form.errors.as_data()[key]:
            errors.append(error.message)
    return errors


@require_http_methods(["GET"])
def home_view(request):
    """Home view"""
    posts = Post.objects.all().order_by("-created_at")
    page = request.GET.get("page", 1)
    paginator = Paginator(posts, 5)
    try:
        paginated_posts = paginator.page(page)
    except PageNotAnInteger:
        paginated_posts = paginator.page(1)
    except EmptyPage:
        paginated_posts = paginator.page(paginator.num_pages)

    community_obj = Community.objects.all().order_by("-pk")[:5]

    return render(
        request,
        "home.html",
        {"communities": community_obj, "posts": paginated_posts},
    )
