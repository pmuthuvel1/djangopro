from django import template

register = template.Library()

@register.filter(is_safe=True)
def service_format(lstr):
    result = ''
    if 'is running' in lstr:
        result = '<i class=\'fa fa-thumbs-up c_green\'></i>'
    elif 'is not running' in lstr:
        result += '<i class=\'fa fa-thumbs-down c_red\'></i>'
    else:
        result += '<i class=\'fa fa-exclamation-triangle c_yellow\'></i>'
    return result

