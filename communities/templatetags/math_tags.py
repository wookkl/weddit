from django import template

register = template.Library()


@register.filter
def mul(value, arg):
    print(value, arg)
    return value * arg


@register.filter
def sub(value, arg):
    print(value, arg)
    return value - arg
