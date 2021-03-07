from django.http import HttpResponseBadRequest

from .models import Comment


def comment_ownership_required(func):
    """Comment ownership requirement decorator definition"""

    def decorated(request, pk):
        comment = Comment.objects.get(pk=pk)
        if comment.writer != request.user:
            return HttpResponseBadRequest()
        return func(request, pk)

    return decorated
