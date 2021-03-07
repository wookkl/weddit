from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect

from .models import Subscription
from communities.models import Community


@login_required
def subscription_toggle_view(request):
    """Subscription toggle view"""
    if request.method == "POST":
        next_url = request.GET.get("next", None)
        community_pk = request.POST.get("community_pk", None)
        try:
            community = Community.objects.get(pk=community_pk)
        except Community.DoesNotExist:
            return Http404()
        try:
            subscription = Subscription.objects.get(
                subscriber=request.user, community=community
            )
            subscription.delete()
        except Subscription.DoesNotExist:
            Subscription.objects.create(subscriber=request.user, community=community)
        if next_url:
            return redirect(next_url)
        else:
            return redirect(community.get_absolute_url())
    return HttpResponseBadRequest()
