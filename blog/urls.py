from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('article/<int:pk>/', views.detail, name='detail'),
    path('articles/archive/<int:year>/<int:month>/<int:day>/', views.archive_day, name='archive-day'),
    path('articles/archive/<int:year>/<int:month>/', views.archive, name='archive'),
    path('articles/category/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('articles/author/<int:pk>/', views.AuthorView.as_view(), name='posts-by-author'),
    path('articles/tag/<int:pk>/', views.TagView.as_view(), name='tag'),
]