from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.urls import reverse
from django.shortcuts import redirect

from .models import Subscription
from communities.models import Community


@method_decorator(login_required, name="dispatch")
class SubscriptionToggleView(View):
    """Subscription toggle view"""

    model = Subscription

    def post(self, request, *args, **kwargs):
        try:
            community = Community.objects.get(pk=kwargs.get("community_pk"))
        except Community.DoesNotExist:
            return Http404()
        try:
            subscription = Subscription.objects.get(
                subscriber=self.user, community=community
            )
            subscription.delete()
        except Subscription.DoesNotExist:
            Subscription.objects.create(subscriber=self.user, community=community)

        return redirect(community.get_absolute_url())
