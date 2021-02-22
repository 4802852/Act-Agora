import re

from django import template

register = template.Library()


@register.filter
def add_link(value):
    content = value.content
    hashtags = value.hashtag.all()

    for tag in hashtags:
        content = re.sub(r'\#' + tag.name + r'\b',
                         '<a href="/post/explore/tags/' + tag.name + '">#' + tag.name + '</a>', content)
    return content
