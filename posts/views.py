from django.views.generic import CreateView, ListView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _

from .models import Post
from .forms import PostForm


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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, "request"):
            kwargs.update({"request": self.request})
        return kwargs

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
