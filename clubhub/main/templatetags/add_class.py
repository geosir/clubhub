# add_class - A template tag to add the given classes to a DOM object's classes.
from django import template

register = template.Library()


@register.filter(name='add_class')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})
