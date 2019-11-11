import markdown
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse

from django.contrib.auth.models import User

from .models import Post, Category, Tag


def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    context = {
        'post_list': post_list,
    }
    template = 'blog/index.html'
    return render(request, template_name=template, context=context)


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    post.body = md.convert(post.body)
    post.toc = md.toc
    post.reads = post.reads + 1
    post.save()
    return render(request, "blog/detail.html", context={'post': post})


def __render(req: HttpRequest, context: dict = dict(), template: str = 'blog/index.html', ) -> HttpResponse:
    return render(req, template_name=template, context=context)


def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    )
    return __render(request, {'post_list': post_list})


def archive_day(request, year, month, day=None):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month,
                                    created_time__day=day
                                    )
    return __render(request, {'post_list': post_list})

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return __render(request, context={'post_list': post_list})

def author(request, pk):
    auth = get_object_or_404(User, pk=pk)
    post_list = Post.objects.filter(author=auth)
    return __render(request, context={'post_list': post_list})

def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t)
    return __render(request, context={'post_list': post_list})
