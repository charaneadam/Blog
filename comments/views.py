from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from blog.models import Post
from .forms import CommentForm

@require_POST
def comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

        messages.success(request ,'Comment added successfully')
        return redirect(post)

    context = {
        'form': form,
        'post': post,
    }

    messages.error(request, 'Comment was not published. Please resubmit after taking care of the errors.')

    template = 'comments/preview.html'

    return render(request, template_name=template, context=context)