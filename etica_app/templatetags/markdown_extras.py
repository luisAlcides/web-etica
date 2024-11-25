import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    html = markdown.markdown(text, extensions=['extra', 'codehilite'])
    return mark_safe(html)
