from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.views.generic import CreateView, ListView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _

from communities.models import Community

from .models import Post
from .forms import PostForm
from .decorators import post_ownership_required


class PostListView(ListView):
    """Post list view definition:"""

    model = Post
    queryset = Post.objects.all()
    paginate_by = 10
    paginate_orphans = 5
    template_name = "posts/list.html"
    ordering = ["-id"]
    http_method_names = ["get"]


@method_decorator(login_required, "get")
@method_decorator(login_required, "post")
class PostCreateView(CreateView, SuccessMessageMixin):
    """Post create view definition"""

    model = Post
    form_class = PostForm
    template_name = "posts/create.html"
    success_message = _("Post created successfully")

    def form_valid(self, form):
        form.instance.writer = self.request.user
        community_pk = self.kwargs["community_pk", None]
        try:
            form.instance.community = Community.objects.get(pk=community_pk)
        except Community.DoesNotExist:
            return HttpResponseBadRequest()
        return super().form_valid(form)

    def form_invalid(self, form):
        errors = []
        for key in form.errors.as_data().keys():
            for error in form.errors.as_data()[key]:
                errors.append(error.message)
        return self.render_to_response(self.get_context_data(form=form, errors=errors))


class PostDetailView(DetailView):
    """Post detail view definition"""

    model = Post
    template_name = "posts/detail.html"
    context_object_name = "post_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_obj = context.get("post_obj")
        is_subscribed = (
            self.request.user.subscriptions.all()
            .filter(subscriber=self.request.user, community=post_obj.community)
            .exists()
        )

        if is_subscribed:
            post_obj.is_subscribed = True
        else:
            post_obj.is_subscribed = False
        context["post_obj"] = post_obj
        return context


@login_required
@post_ownership_required
def post_delete_view(request, pk):
    return render(request, "posts/delete.html", {"pk": pk}, status=200)


@login_required
@post_ownership_required
def post_delete_confirm_view(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        post.delete()
    except Post.DoesNotExist:
        return HttpResponseBadRequest()
    return redirect(reverse("posts:list"))
