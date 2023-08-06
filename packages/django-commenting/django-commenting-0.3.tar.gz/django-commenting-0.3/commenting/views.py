from django.shortcuts import render, redirect
from .forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, HttpResponseRedirect
from .models import Comment

# Create your views here.
def postcomments(request):
    comment_form = CommentForm()
    
    if request.method == 'POST':
        # print(request.POST)
        model_name = request.POST.get('model_name')
        object_id = request.POST.get('object_id')

        content_type = ContentType.objects.get(model=model_name.lower())
        # print(content_type)
    #     # A comment was posted
        comment_form = CommentForm(data=request.POST)
        
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            new_comment.content_type = content_type
            new_comment.object_id = object_id
            new_comment.save()
            # absolutepath = request.build_absolute_uri()
            absolutepath = request.META.get('HTTP_REFERER')
            path =  absolutepath+'#'+str(new_comment.id)
        return redirect(path)
    return redirect(absolutepath)


def postreply(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        model_name = request.POST.get('model_name')
        content_type = ContentType.objects.get(model=model_name.lower())
        if form.is_valid():
            post_id = request.POST.get('post_id')  # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            # post_url = request.POST.get('post_url')  # from hidden input

            reply = form.save(commit=False)
            reply.content_type = content_type
            reply.object_id = post_id
            reply.parent = Comment(id=parent_id)
            reply.save()
        
        absolutepath = request.META.get('HTTP_REFERER')
        path =  absolutepath+'#'+str(reply.id)
        return redirect(path)

    return redirect(absolutepath)
