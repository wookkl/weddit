from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest
from django.views.generic import CreateView, ListView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.views.generic.edit import FormMixin

from .models import Post
from .forms import PostForm
from comments.forms import CommentForm
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
class PostCreateView(SuccessMessageMixin, CreateView):
    """Post create view definition"""

    model = Post
    form_class = PostForm
    template_name = "posts/create.html"
    success_message = _("Post created successfully")

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
    context_object_name = "post_obj"

    form_class = CommentForm


@login_required
@post_ownership_required
def post_delete_view(request, pk):
    nxt = request.GET.get("next", None)
    try:
        post = Post.objects.get(pk=pk)
        post.delete()
    except Post.DoesNotExist:
        return HttpResponseBadRequest()
    if nxt:
        return redirect(nxt)
    return redirect(reverse("home"))
