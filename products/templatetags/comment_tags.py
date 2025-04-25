from django import template

register = template.Library()


@register.filter
def only_active_comments(comments):
    """
    Filter to get only active comments.
    """
    return comments.filter(active=True)  # or -> comments.exclude(active=False)
