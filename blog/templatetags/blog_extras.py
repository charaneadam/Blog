from django import template

from blog.models import Post, Category, Tag

register = template.Library()

@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_posts_list': Post.objects.all()[:num]
    }


def __get_posts_dates_by_time_constraint(constraint):
    return Post.objects.dates('created_time', constraint, order='DESC')


@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context, constraint='month'):
    return {
        'date_list': __get_posts_dates_by_time_constraint(constraint),
    }


@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    return {
        'category_list': Category.objects.all(),
    }


@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tag_list': Tag.objects.all(),
    }
