from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect

from posts.models import Post

from .models import Vote


@login_required
def vote_toggle_view(request):
    """vote toggle view"""

    if request.method == "GET":
        next_url = request.GET.get("next", None)
        post_pk = request.GET.get("pk", None)
        status = request.GET.get("status", None)

        if status != "up" and status != "down":
            return HttpResponseBadRequest()

        like = True if status == "up" else False

        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            return Http404()

        if Vote.objects.filter(voter=request.user, post=post).exists():
            vote = Vote.objects.get(voter=request.user, post=post)

            if vote.like == like:
                vote.delete()
            else:
                vote.like = like
                vote.save()

            if next_url:
                return redirect(next_url)
            else:
                return redirect(post.get_absolute_url())

        Vote.objects.create(voter=request.user, post=post, like=like)

        if next_url:
            return redirect(next_url)
        else:
            return redirect(post.get_absolute_url())

    return HttpResponseBadRequest()
