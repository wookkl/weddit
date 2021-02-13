from django.http import HttpResponseBadRequest

from .models import Post


def post_ownership_required(func):
    """Post ownership requirement decorator definition"""

    def decorated(request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs["pk"])
        if post.writer != request.user:
            return HttpResponseBadRequest
        return func(request, *args, **kwargs)

    return decorated
