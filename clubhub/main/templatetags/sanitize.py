# sanitize - Escape HTML except for some allowed tags.
import re
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


def sanitize(text):
    replacements = {
        "&lt;b&gt;": "<b>",
        "&lt;/b&gt;": "</b>",
        "&lt;i&gt;": "<i>",
        "&lt;/i&gt;": "</i>",
        "&lt;u&gt;": "<u>",
        "&lt;/u&gt;": "</u>",
        "&lt;s&gt;": "<s>",
        "&lt;/s&gt;": "</s>",
        "&lt;/a&gt;": "</a>",
        "&nbsp;": "<br />",
        "\n": "<br />"
    }

    safetext = escape(text)
    for r in replacements:
        safetext = safetext.replace(r, replacements[r])

    # Handle <a href="..."> tags
    safetext = re.sub(r'&lt;a href=&quot;([^"<>]+)&quot;&gt;', r'<a href="\1">', safetext)

    return mark_safe(safetext)


register.filter("sanitize", sanitize)
