from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest

from .models import Comment


def comment_ownership_required(func):
    """Comment ownership requirement decorator definition"""

    @wraps(func)
    def wrapper(request, pk):
        comment = Comment.objects.get(pk=pk)
        if comment.writer != request.user:
            return HttpResponseBadRequest()

        wrapped = login_required(func)
        return wrapped(request, pk)

    return wrapper
