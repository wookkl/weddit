from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from communities.models import Community
from posts.models import Post


def get_filtered_objects(query, model, page=None):
    if model == get_user_model():
        objs = model.objects.filter(Q(nickname__icontains=query))
    elif model == Community:
        objs = model.objects.filter(
            Q(name__icontains=query)
            | Q(title__icontains=query)
            | Q(description__icontains=query)
        )
    elif model == Post:
        objs = model.objects.filter(Q(content__icontains=query))
    if page:
        paginator = Paginator(objs, 10)
        try:
            paginated_objs = paginator.page(page)
        except PageNotAnInteger:
            paginated_objs = paginator.page(1)
        except EmptyPage:
            paginated_objs = paginator.page(paginator.num_pages)
        return paginated_objs
    return objs


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
    print(paginated_posts)
    return render(
        request,
        "home.html",
        {"communities": community_obj, "posts": paginated_posts},
    )


@require_http_methods(["GET"])
def search_view(request):
    """Search view"""
    contexts = {}

    if request.method == "GET":
        page = request.GET.get("page", 1)
        typee = request.GET.get("type", None)
        query = request.GET.get("q", "")
        if typee is None:
            contexts["users"] = get_filtered_objects(query, get_user_model())[:3]
            contexts["communities"] = get_filtered_objects(query, Community)[:3]
            contexts["posts"] = get_filtered_objects(query, Post)[:3]
        elif typee == "comm":
            contexts["communities"] = get_filtered_objects(query, Community, page=page)
        elif typee == "user":
            contexts["users"] = get_filtered_objects(query, get_user_model(), page=page)
        elif typee == "post":
            contexts["posts"] = get_filtered_objects(query, Post, page=page)
        contexts["type"] = typee
        contexts["query"] = query
        return render(
            request,
            "core/search.html",
            contexts,
            status=200,
        )
    else:
        return HttpResponseBadRequest()
