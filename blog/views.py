from django.shortcuts import render
from django.http import HttpResponse

from .models import Post


def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    context = {
        'post_list': post_list,
    }
    template = 'blog/index.html'
    return render(request, template_name=template, context=context)
