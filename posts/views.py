from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.views.generic.edit import FormMixin

from .models import Post
from .forms import PostCreateForm, PostUpdateForm
from .decorators import post_ownership_required

from comments.forms import CommentForm


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


class PostListView(ListView):
    """Post list view definition:"""

    model = Post
    paginate_by = 10
    paginate_orphans = 5
    template_name = "posts/list.html"
    ordering = ["-id"]
    http_method_names = ["get"]


@method_decorator(login_required, "get")
@method_decorator(login_required, "post")
class PostCreateView(SuccessMessageMixin, CreateView):
    """Post create view definition"""

    model = Post
    form_class = PostCreateForm
    template_name = "posts/create.html"
    success_message = _("Post created successfully")

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(user=self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        if not self.request.user.can_create_community:
            if self.request.user.posts.count() >= 20:
                if self.request.user.comments.count() >= 100:
                    self.request.user.can_create_community = True
                    self.request.user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        errors = []
        for key in form.errors.as_data().keys():
            for error in form.errors.as_data()[key]:
                errors.append(error.message)
        return self.render_to_response(self.get_context_data(form=form, errors=errors))


@method_decorator(login_required, "get")
@method_decorator(login_required, "post")
class PostUpdateView(SuccessMessageMixin, UpdateView):
    """Post update view definition"""

    model = Post
    form_class = PostUpdateForm
    template_name = "posts/update.html"
    success_message = _("Post updated successfully")

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(user=self.request.user, **self.get_form_kwargs())

    def form_invalid(self, form):
        errors = []
        for key in form.errors.as_data().keys():
            for error in form.errors.as_data()[key]:
                errors.append(error.message)
        return self.render_to_response(self.get_context_data(form=form, errors=errors))


class PostDetailView(FormMixin, DetailView):
    """Post detail view definition"""

    model = Post
    template_name = "posts/detail.html"
    context_object_name = "post"
    form_class = CommentForm
    queryset = (
        Post.objects.prefetch_related("comments").prefetch_related("community").all()
    )
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        user_ip = get_client_ip(request)
        cached_visitors_key = f"post_{post.pk}_visitors_"
        post_visitors_keys = cache.keys(cached_visitors_key + "*")
        if post_visitors_keys:
            ips = [cache.get(key) for key in post_visitors_keys]
            if user_ip not in ips:
                post.hits += 1
                post.save()
                cache.set(f"{cached_visitors_key}{post.hits}", user_ip, timeout=60 * 60)
        else:
            post.hits += 1
            post.save()
            cache.set(f"{cached_visitors_key}{post.hits}", user_ip, timeout=60 * 60)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = self.get_related_comments()
        context["comments"] = comments
        return context

    def get_related_comments(self):
        queryset = self.object.comments.all().order_by("created_at")
        paginator = Paginator(queryset, 5)
        page = self.request.GET.get("page", 1)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
        return comments


@login_required
@post_ownership_required
def post_delete_view(request, pk):
    if request.method == "POST":
        try:
            post = Post.objects.get(pk=pk)
            post.delete()
            cached_visitors_key = f"post_{pk}_visitors_"
            post_visitors_keys = cache.keys(cached_visitors_key + "*")
            if post_visitors_keys:
                cache.delete_pattern(post_visitors_keys)
        except Post.DoesNotExist:
            return HttpResponseBadRequest()
        return redirect(reverse("home"))
    else:
        return HttpResponseBadRequest()
