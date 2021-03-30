from django import template

from subscriptions.models import Subscription


register = template.Library()


@register.simple_tag
def is_subscribed(subscriber, community):
    return Subscription.objects.filter(
        subscriber=subscriber, community=community
    ).exists()


@register.simple_tag
def get_photo_url_or_none(object):
    try:
        url = object.get_photo_url()
    except ValueError:
        url = None
    return url


@register.simple_tag
def get_avatar_url_or_none(object):
    try:
        url = object.get_avatar_url()
    except ValueError:
        url = None
    return url
