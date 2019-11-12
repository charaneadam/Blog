import markdown
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView
from django.contrib.auth.models import User

from .models import Post, Category, Tag


class IndexView(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'blog/index.html'


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class AuthorView(IndexView):
    def get_queryset(self):
        auth = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return super(AuthorView, self).get_queryset().filter(author=auth)


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if day:
            return Post.objects.filter(created_time__year=year, created_time__month=month, created_time__day=day)
        return Post.objects.filter(created_time__year=year, created_time__month=month)


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
