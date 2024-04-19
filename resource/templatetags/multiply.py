from django import template

register = template.Library()


@register.filter
def append_str(value, arg):
    """Removes all values of arg from the given string"""
    return value + arg


@register.filter
def mult(value, arg):
    return int(value) * int(arg)

