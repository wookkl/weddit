from django.http import Http404
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from .forms import CommentForm
from .models import Comment
from posts.models import Post
from core.views import get_form_errors


@method_decorator(login_required, "get")
@method_decorator(login_required, "post")
class CreateCommentView(CreateView):
    """Create comment view definition"""

    form_class = CommentForm
    model = Comment
    template_name = "comments/create.html"

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = Post.objects.get(pk=self.request.POST["post_pk"])
        comment.writer = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("posts:detail", kwargs={"pk": self.object.post.pk})
