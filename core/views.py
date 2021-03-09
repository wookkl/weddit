from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.contrib.auth import get_user_model
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


@require_http_methods(["GET"])
def search_view(request):
    """Search view"""
    users = None
    communities = None
    posts = None
    if request.method == "GET":
        typee = request.GET.get("type", None)
        query = request.GET.get("q", None)
        if typee is None:
            users = get_user_model().objects.filter(Q(nickname__icontains=query))[:3]
            communities = sorted(
                Community.objects.filter(
                    Q(name__icontains=query)
                    | Q(title__icontains=query)
                    | Q(description__icontains=query)
                ),
                key=lambda x: x.get_subscriber_count(),
                reverse=True,
            )[:3]
            posts = Post.objects.filter(Q(content__icontains=query))
        elif typee == "comm":
            communities = Community.objects.filter(
                Q(name__icontains=query)
                | Q(title__icontains=query)
                | Q(description__icontains=query)
            )
        elif typee == "user":
            users = get_user_model().objects.filter(Q(nickname__icontains=query))
        elif typee == "post":
            posts = Post.objects.filter(Q(content__icontains=query))
        return render(
            request,
            "core/search.html",
            {
                "users": users,
                "communities": communities,
                "posts": posts,
                "query": query,
            },
            status=200,
        )
    else:
        return HttpResponseBadRequest()
