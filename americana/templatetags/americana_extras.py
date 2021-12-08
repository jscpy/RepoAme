from django import template

register = template.Library()

@register.filter()
def to_int(value):
    if value == '':
        return 1
    else:
        return int(value)
