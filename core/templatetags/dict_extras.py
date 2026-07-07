from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    """
    Safely get a value from a dictionary in templates.
    Usage: {{ mydict|dict_get:somekey }}
    """
    if d and key in d:
        return d.get(key)
    return ""
