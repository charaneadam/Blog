import markdown
from django.shortcuts import render, get_object_or_404
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

############################# TODO: Turn these views to class based views #############################
def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    )
    return __render(request, {'post_list': post_list})

class ArchiveView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, year=self.kwargs.get('year'), month=self.kwargs.get('month'))
        return super(ArchiveView, self).get_queryset().filter(category=cate)

def archive_day(request, year, month, day=None):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month,
                                    created_time__day=day
                                    )
    return __render(request, {'post_list': post_list})

############################# TODO (END): Turn these views to class based ...  #############################



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

