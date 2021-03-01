from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView

from .forms import CommentForm
from .models import Comment
from .decorators import comment_ownership_required
from posts.models import Post


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


class CommentDetailView(DetailView):
    """ Comment detail view definition"""

    model = Comment
    template_name = "comments/detail.html"


@login_required
@comment_ownership_required
def comment_delete_view(request, pk):
    nxt = request.GET.get("next", None)
    print(nxt)
    if request.method == "POST":
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()
            if nxt:
                return redirect(nxt)
        except comment.DoesNotExist:
            return HttpResponseBadRequest()
    return HttpResponseBadRequest()
