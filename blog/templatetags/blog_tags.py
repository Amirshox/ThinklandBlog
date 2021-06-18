from django import template

from ..models import Category

register = template.Library()


@register.simple_tag
def categories():
    return Category.objects.all()
