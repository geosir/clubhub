# get_timezones - Returns a list of timezones.
import pytz
from django import template

register = template.Library()

@register.simple_tag
def get_timezones():
    return pytz.common_timezones