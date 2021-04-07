from functools import wraps
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest

from .models import Post


def post_ownership_required(func):
    """Post ownership requirement decorator definition"""

    @wraps(func)
    def wrapper(request, pk):
        post = Post.objects.get(pk=pk)
        if post.writer != request.user:
            return HttpResponseBadRequest()

        wrapped = login_required(func)
        return wrapped(request, pk)

    return wrapper
