from django import template
from commenting.models import Comment
from django.contrib.contenttypes.models import ContentType
from commenting.forms import CommentForm

register = template.Library()

@register.simple_tag
def allcomments(object):
    modal_name = object._meta.model_name
    c_type = None
    try:
        c_type =  ContentType.objects.get(model=modal_name.lower())
    except ContentType.DoesNotExist:
        return None
    if c_type:
        all_comments = Comment.objects.filter(content_type=c_type, object_id=object.id)
    return all_comments

@register.simple_tag(takes_context=True)
def get_comment_form(context):
    request = context['request']
    comment_form = CommentForm(request.POST or None)
    return comment_form

# @register.filter
# def get_content_type(model_name):
    
@register.filter
def get_model_name(obj):
    return obj._meta.model_name