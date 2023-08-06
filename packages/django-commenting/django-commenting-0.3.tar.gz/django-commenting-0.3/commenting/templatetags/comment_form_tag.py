from django import template
from django.template.loader import render_to_string

register = template.Library()

# @register.simple_tag
# def render_comment_form(object):
#     context = {
#         'object': object,
#     }
#     return render_to_string('comment-form.html', context)

@register.simple_tag(takes_context=True)
def render_comment_form(context, object):
    request = context['request']
    # Use the request object as needed
    # ...

    template = 'comment-form.html'
    context = {
        'object': object,
    }
    return render_to_string(template, context, request=request)