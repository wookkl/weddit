from django.http import HttpResponseBadRequest

from .models import Comment


def comment_ownership_required(func):
    """Comment ownership requirement decorator definition"""

    def decorated(request, *args, **kwargs):
        comment = Comment.objects.get(pk=kwargs["pk"])
        if comment.writer != request.user:
            return HttpResponseBadRequest
        return func(request, *args, **kwargs)

    return decorated
