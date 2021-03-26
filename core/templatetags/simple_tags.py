from django import template

from subscriptions.models import Subscription

register = template.Library()


@register.simple_tag
def is_subscribed(subscriber, community):
    return Subscription.objects.filter(
        subscriber=subscriber, community=community
    ).exists()
