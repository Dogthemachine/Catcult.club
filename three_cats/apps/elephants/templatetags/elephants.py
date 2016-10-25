from django import template

from apps.elephants.models import Sizes


register = template.Library()


@register.simple_tag
def get_size_desc(size_id):
    try:
        size = Sizes.objects.get(id=size_id)
    except:
        return ''

    return size.description